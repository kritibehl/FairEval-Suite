import torch.nn as nn

class TinyTextClassifier(nn.Module):
    def __init__(self, vocab_size=128, embed_dim=16, num_classes=3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.classifier = nn.Linear(embed_dim, num_classes)

    def forward(self, token_ids):
        emb = self.embedding(token_ids).mean(dim=1)
        return self.classifier(emb)
