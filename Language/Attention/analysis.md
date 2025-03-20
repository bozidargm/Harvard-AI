# Analysis

For this task, we will use the same sentence with two same words in it but with different meanings (homonyms) to follow how BERT will manage in such a situation. In one sentence, the homonym is masked, while in the other, the noun that the homonym determines is masked.

Example Sentences:
- The bank is located on the [MASK] of the river.
- The bank is located on the bank of the [MASK].

**the bank** - building
**bank** - river bank

## Layer 1, Head 2

In this head, in the sentence where bank is masked (hereafter [bank]), special attention is paid to the intersection of the masked word, but it is also seen that the relationship between **the bank** and river is taught.

In the sentence [river], the relationship between river and **the bank** is not examined, attention is paid only to the intersection of the masked word.

## Layer 1, Head 8 & Layer 3, Head 11 & Layer 4, Head 9

In sentence [bank] the relationship between **the bank** and river is examined, but not in the sentence [river]

## Layer 5, Head 7

In sentence [river] special attention is paid on "the [MASK]" relationship with **bank** while this attention is not paid in sentence [bank].


## Layer 10, Head 10

In this head, there is strong signal of attention between [MASK] (**bank**) and river in sentence [bank] while in sentence [river] attention is paid on [MASK] and previous word (the).