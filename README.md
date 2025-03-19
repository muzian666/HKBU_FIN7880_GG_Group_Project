# New Branch

This is new branch of this project, we are going to apply reasoning model for better solution.

## Method
Well... No matter which Approach, clean the data is first step...... :-(

The documents are really really old.... And some formular even cannot been convert.... So strange....

Using olmOCR for convert documents.

### Simple Approach: Distill from DeepSeek R1
#### Step 1: Use DeepSeek to Extend the Chain of Thougt.
This step is simple, just put the question into DeepSeek R1 and let it generate the Chain of Thought, and then record them.

The Dataset will upload to Huggingface.


### Hard Approach: SFT + GRPO, repeat DeepSeek R1 Zero
#### Step 1: Rebuild Dataset
Our target dataset is the after class Assignment for Class FIN 7870 Financial Derivatives and Risk Managment. The original dataset is in Word formate and all the question and answer are mix together.

For example:
```
An investor enters into a short forward contract to sell 100,000 British pounds for US  dollars at an exchange rate of 1.5000 US dollars per pound. How much does the investor gain or lose if the exchange rate at the end of the contract is (a) 1.4900 and (b) 1.5200? 

(a)	The investor is obligated to sell pounds for 1.5000 when they are worth 1.4900. The gain is (1.5000−1.4900) ×100,000 = $1,000.

(b)	The investor is obligated to sell pounds for 1.5000 when they are worth 1.5200. The loss is (1.5200−1.5000)×100,000 = $2,000
```

For above question and answer pair, it is actually two question with two answers. So we need to seperate it.

For example:
```json
[
    {
        "question": "An investor enters into a short forward contract to sell 100,000 British pounds for US  dollars at an exchange rate of 1.5000 US dollars per pound. How much does the investor gain or lose if the exchange rate at the end of the contract is 1.4900?",
        "answer": "The investor is obligated to sell pounds for 1.5000 when they are worth 1.4900. The gain is (1.5000−1.4900) ×100,000 = $1,000.",
        "extract_answer": "$1,000"
    },
    {
        "question": "An investor enters into a short forward contract to sell 100,000 British pounds for US  dollars at an exchange rate of 1.5000 US dollars per pound. How much does the investor gain or lose if the exchange rate at the end of the contract is 1.5200? ",
        "answer": "The investor is obligated to sell pounds for 1.5000 when they are worth 1.5200. The loss is (1.5200−1.5000)×100,000 = $2,000",
        "extract_answer": "$2,000"
    }
]
```

The reason why we need `extract_answer` is for GRPO to build the reward function, which the extract_answer is correct with 
