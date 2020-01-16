import random
import numpy as np
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
import pickle
from src.utils import align

class PreModel(nn.Module):
    def __init__(self):
        super(PreModel, self).__init__()
        self.MD = nn.ModuleDict({
            "encoder": BertModel.from_pretrained('bert-base-uncased'),
            # "query_encoder": BertModel.from_pretrained('bert-base-uncased'),
            # "db_encoder": BertModel.from_pretrained('bert-base-uncased'),
            "linear1": nn.Linear(768, 768),
            "linear2": nn.Linear(768, 300),
            "linear3": nn.Linear(300, 1)
        })
        
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.db_dict = pickle.load(open('save/DB_tok', 'rb'))
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        
        for submodel in [self.MD["encoder"]]:
            for param in submodel.parameters():
                param.requires_grad = False
                
    def dataprocess(self, batch):
        db = []
        tk = []
        num = len(batch.question)
        for id, qstr in enumerate(batch.question):
            qst = align(self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(qstr)), 128)
            dbs = self.db_dict[batch.dbid[id]]
            tks = [0] * len(qst) + [1] * len(dbs)
            db.append(qst + dbs)
            tk.append(tks)
        return torch.tensor(db).to(self.device), torch.tensor(tk).to(self.device)
        
    
    def forward(self, x):
        db, tok = self.dataprocess(x)
        x = self.MD['encoder'](db, token_type_ids=tok)
        # Q = self.MD["query_encoder"](query)
        # D = self.MD["db_encoder"](db)
#         x = torch.sum(Q[0][:, 0, :] * D[0][:, 0, :], axis=-1)
#         print(x)
        # x = torch.cat([Q[0][:, 0, :], D[0][:, 0, :]], -1)
        x = torch.nn.functional.relu(self.MD["linear1"](x[0][:, 0, :]))
        x = torch.nn.functional.relu(self.MD["linear2"](x))
        # x = self.MD["linear3"](x)
        return x