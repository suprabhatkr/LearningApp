import logging
from typing import List, Dict, Any, Optional
from elasticsearch import AsyncElasticsearch
from app.config import settings

logger = logging.getLogger("Search")

class InMemorySearchEngine:
    """Fallback search engine simulating Elasticsearch query syntax and highlighting using simple token matching."""
    def __init__(self):
        self._indices: Dict[str, List[Dict[str, Any]]] = {}
        logger.info("Initializing In-Memory Search Engine (Elasticsearch Offline Fallback)")

    def index_document(self, index: str, doc_id: str, document: Dict[str, Any]):
        if index not in self._indices:
            self._indices[index] = []
        # Update if exists, else append
        document = dict(document)  # Copy
        document["id"] = doc_id
        self._indices[index] = [d for d in self._indices[index] if d["id"] != doc_id]
        self._indices[index].append(document)

    def search(self, index: str, query: str, fields: List[str]) -> List[Dict[str, Any]]:
        if index not in self._indices or not query:
            return []
        
        query_tokens = query.lower().split()
        results = []
        
        for doc in self._indices[index]:
            score = 0
            highlights = {}
            match_found = False
            
            for field in fields:
                field_val = str(doc.get(field, "")).lower()
                field_orig = str(doc.get(field, ""))
                
                # Check for token overlap
                token_matches = 0
                for token in query_tokens:
                    if token in field_val:
                        token_matches += 1
                        
                if token_matches > 0:
                    score += token_matches * 10
                    match_found = True
                    
                    # Highlight matches in original field text
                    highlighted_text = field_orig
                    # Basic case-insensitive replacement (highly simplified)
                    for token in query_tokens:
                        start_idx = highlighted_text.lower().find(token)
                        if start_idx != -1:
                            end_idx = start_idx + len(token)
                            orig_word = highlighted_text[start_idx:end_idx]
                            highlighted_text = highlighted_text[:start_idx] + f"<em>{orig_word}</em>" + highlighted_text[end_idx:]
                    
                    highlights[field] = [highlighted_text]
            
            if match_found:
                results.append({
                    "_source": doc,
                    "_score": score,
                    "highlight": highlights
                })
        
        # Sort by score descending
        results.sort(key=lambda x: x["_score"], reverse=True)
        return results


class SearchManager:
    def __init__(self):
        self.es: Optional[AsyncElasticsearch] = None
        self.local_search = InMemorySearchEngine()
        self.is_es_active = False

    async def connect(self):
        try:
            self.es = AsyncElasticsearch(
                hosts=[settings.ELASTICSEARCH_HOST],
                request_timeout=1.0  # Fail fast
            )
            # Try to ping the cluster
            await self.es.ping()
            self.is_es_active = True
            logger.info("Connected to Elasticsearch successfully.")
        except Exception as e:
            logger.warning(f"Elasticsearch connection failed: {e}. Falling back to in-memory search.")
            self.es = None
            self.is_es_active = False

    async def index_document(self, index: str, doc_id: str, document: Dict[str, Any]):
        """Index a document in Elasticsearch, or fallback to in-memory index."""
        if self.is_es_active and self.es:
            try:
                await self.es.index(index=index, id=doc_id, document=document)
                return
            except Exception as e:
                logger.error(f"Elasticsearch index error: {e}. Writing to fallback.")
        self.local_search.index_document(index, doc_id, document)

    async def search(self, index: str, query: str, fields: List[str]) -> List[Dict[str, Any]]:
        """
        Execute a search with Elasticsearch using Multi-match query with fuzziness and highlighting.
        Highly educational senior SDE pattern.
        """
        if self.is_es_active and self.es:
            try:
                # Query body illustrating multi_match, fuzziness and highlights
                body = {
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": fields,
                            "fuzziness": "AUTO"
                        }
                    },
                    "highlight": {
                        "fields": {
                            field: {} for field in fields
                        },
                        "pre_tags": ["<em>"],
                        "post_tags": ["</em>"]
                    }
                }
                response = await self.es.search(index=index, body=body)
                hits = response.get("hits", {}).get("hits", [])
                
                # Format hits to match fallback shape
                formatted_hits = []
                for hit in hits:
                    formatted_hits.append({
                        "_source": hit["_source"],
                        "_score": hit["_score"],
                        "highlight": hit.get("highlight", {})
                    })
                return formatted_hits
            except Exception as e:
                logger.error(f"Elasticsearch search error: {e}. Reading from fallback search.")
                
        # Return fallback results
        return self.local_search.search(index, query, fields)

search_manager = SearchManager()
