# Dialogue Agent Conversation Alignment

This is Natalie Nova's undergraduate Thesis project code. 

## Installation

In order to run the code start by downloading Rasa. 

```bash
pip3 install -U --user pip && pip3 install rasa
```
This makes sure you have the most up to date version of pip. 

Next run this command
```bash
 rasa init
```
This will walk you through the steps of making your inital agent. Go through all the steps and make sure this is working properly before moving on. 
This step is just to make sure everything is running smoothly and the installation went well. Keep these files in a seperate folder.

## Usage
Clone the repository 

In one terminal write the command: 
```bash
 rasa train 
```
Open another terminal window and type in the command: 
```bash
 rasa run actions 
```
When the model has completed training in the same terimal window where the training was just completed type the command: 
```bash
 rasa shell
```
This will allow you to have a conversation with the agent. 

If you would like to test the agent based on the stories in the testing file type: 
```bash
 rasa test 
```

## Addition
The theory for the intent action beam search is in the file beamPolicy.py and there are commented out versions for how to configure for a custom policy. 

