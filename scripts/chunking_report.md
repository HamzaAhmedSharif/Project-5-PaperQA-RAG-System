# Chunking Strategy Comparison Report
**PDF**: pdf for upload test.pdf  **Embedding Model**: BAAI/bge-small-en-v1.5  **Overlap Sentences**: 2  **Test Questions**: 3  **Top-K Retrieved**: 3  
## Chunk Size: 300
**Number of chunks**: 230  
### Question 1: What is the main contribution of the Attention Is All You Need paper?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 3 | 0.6268 | 3.2 Attention An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and ... |
| 2 | 14 | 0.6215 | Top: Full attentions for head 5. Bottom: Isolated attentions from just the word ‘its’ for attention heads 5 and 6. Note that the attentions are very s... |
| 3 | 2 | 0.6089 | In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-w... |

### Question 2: How does multi-head attention work?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 4 | 0.8184 | (right) Multi-Head Attention consists of several attention layers running in parallel. of the values, where the weight assigned to each value is compu... |
| 2 | 5 | 0.8020 | 3.2.3 Applications of Attention in our Model The Transformer uses multi-head attention in three different ways: •In "encoder-decoder attention" layers... |
| 3 | 5 | 0.8008 | Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality. 3.2.3 Ap... |

### Question 3: What are the key innovations of the Transformer architecture?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 2 | 0.6871 | To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations o... |
| 2 | 1 | 0.6843 | Ashish, with Illia, designed and implemented the first Transformer models and has been crucially involved in every aspect of this work. Noam proposed ... |
| 3 | 3 | 0.6776 | Figure 1: The Transformer - model architecture. The Transformer follows this overall architecture using stacked self-attention and point-wise, fully c... |

## Chunk Size: 500
**Number of chunks**: 128  
### Question 1: What is the main contribution of the Attention Is All You Need paper?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 3 | 0.6227 | 3.2 Attention An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and ... |
| 2 | 2 | 0.6089 | In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-w... |
| 3 | 14 | 0.5990 | Bottom: Isolated attentions from just the word ‘its’ for attention heads 5 and 6. Note that the attentions are very sharp for this word. 14 Input-Inpu... |

### Question 2: How does multi-head attention work?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 5 | 0.7932 | 3.2.3 Applications of Attention in our Model The Transformer uses multi-head attention in three different ways: •In "encoder-decoder attention" layers... |
| 2 | 5 | 0.7821 | For each of these we use dk=dv=dmodel/h= 64 . Due to the reduced dimension of each head, the total computational cost is similar to that of single-hea... |
| 3 | 4 | 0.7785 | (right) Multi-Head Attention consists of several attention layers running in parallel. of the values, where the weight assigned to each value is compu... |

### Question 3: What are the key innovations of the Transformer architecture?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 2 | 0.6765 | To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations o... |
| 2 | 2 | 0.6694 | The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as l... |
| 3 | 1 | 0.6611 | Listing order is random. Jakob proposed replacing RNNs with self-attention and started the effort to evaluate this idea. Ashish, with Illia, designed ... |

## Chunk Size: 800
**Number of chunks**: 67  
### Question 1: What is the main contribution of the Attention Is All You Need paper?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 3 | 0.5959 | 3.2 Attention An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and ... |
| 2 | 13 | 0.5836 | <EOS> <pad> <pad> <pad> <pad> <pad> <pad> It is in this spirit that a majority of American governments have passed new laws since 2009 making the regi... |
| 3 | 14 | 0.5812 | Bottom: Isolated attentions from just the word ‘its’ for attention heads 5 and 6. Note that the attentions are very sharp for this word. 14 Input-Inpu... |

### Question 2: How does multi-head attention work?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 5 | 0.7767 | Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality. 3.2.3 Ap... |
| 2 | 5 | 0.7765 | output values. These are concatenated and once again projected, resulting in the final values, as depicted in Figure 2. Multi-head attention allows th... |
| 3 | 3 | 0.7441 | 3.2 Attention An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and ... |

### Question 3: What are the key innovations of the Transformer architecture?
| Rank | Page | Similarity | Chunk Preview |
|------|------|------------|---------------|
| 1 | 2 | 0.6656 | To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations o... |
| 2 | 1 | 0.6652 | Listing order is random. Jakob proposed replacing RNNs with self-attention and started the effort to evaluate this idea. Ashish, with Illia, designed ... |
| 3 | 2 | 0.6462 | In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw glob... |

---
*Generated by scripts/evaluate_chunking.py*
