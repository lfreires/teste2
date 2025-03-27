import os
import faiss
import pickle
import numpy as np

class FaissIndex:
    def __init__(self, dim=1536, index_path="data/faiss_index.index", metadata_path="data/faiss_metadata.pkl"):
        self.dim = dim
        self.index_path = index_path
        self.metadata_path = metadata_path

        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.carregar()

    def adicionar(self, vetores, metadados):
        vetores_np = np.array(vetores).astype('float32')
        self.index.add(vetores_np)
        self.metadata.extend(metadados)
        self.salvar()

    def buscar_similares(self, vetor_consulta, top_k=3):
        vetor_np = np.array(vetor_consulta).astype('float32').reshape(1, -1)
        distancias, indices = self.index.search(vetor_np, top_k)

        resultados = []
        for idx, dist in zip(indices[0], distancias[0]):
            if idx < len(self.metadata):
                resultados.append({
                    "distancia": dist,
                    "metadado": self.metadata[idx]
                })
        return resultados

    def salvar(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)
            print('Arquivo salvo!')

    def carregar(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def documento_ja_indexado(self, hash_documento):
        return any(m.get("id_documento") == hash_documento for m in self.metadata)

