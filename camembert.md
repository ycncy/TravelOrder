
# Loss computation
            
```
Loss computation refers to the process of calculating how far off the model’s predictions are from the true (or expected) labels

This loss guides the model during training: the lower the loss, the better the model is at making correct predictions

The goal of training is to minimize this loss
```            

```
In this tokenize_and_align_labels method, we are dealing with token classification for Named Entity Recognition (NER). 

The model is trained to classify each token in a sequence as either part of an entity (like a location, person, etc.) or as “outside” of any entity

During this process, the model needs to compute a loss value for each token’s prediction compared to its actual label
```

### The Purpose of -100

```
Some tokens, like special tokens, don’t correspond to any meaningful labels for entities. 

They are present purely for structuring the input (like separating sentences). 

Since these tokens don’t have relevant labels in the NER context, we need the model to ignore them during loss computation
```

### In the code

```
token_start == token_end: This check indicates a special token, as it has no character span in the original text (it’s not derived from any specific character range).

label_ids.append(-100): Assigning -100 as the label for these tokens tells the model to skip this token when computing loss.
```