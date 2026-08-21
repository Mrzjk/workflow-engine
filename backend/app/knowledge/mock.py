class MockRetriever:
    async def retrieve(self,query,top_k): return [{"content":f"Mock knowledge for: {query}","score":1.0}][:top_k]
