
## Setup

### Install the dependencies

In a Python3 virtual environment run:

```bash
pip install -r requirements.txt
```

To install development dependencies, run:

```bash
pip install -r requirements-dev.txt
```

## Running the bot

Always start by training your model 
```bash
rasa train
```
Once the training is done, run the actions 
```bash
rasa run actions
```

Finally, once everything is running you can speak to the bot
```bash
rasa shell 
```






