from typing import List, Optional, Dict, Text, Any
import numpy as np 
import logging

from torch import argmax

from rasa.core.featurizers.precomputation import MessageContainerForCoreFeaturization
from rasa_sdk.events import UserUttered, BotUttered
from rasa.core.policies.policy import PolicyPrediction, Policy
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.shared.core.domain import Domain
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from rasa.engine.graph import ExecutionContext
from rasa.engine.storage.storage import ModelStorage

from rasa.shared.core.constants import SLOTS, ACTIVE_LOOP, ACTION_UNLIKELY_INTENT_NAME

logger = logging.getLogger(__name__)

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.POLICY_WITH_END_TO_END_SUPPORT, is_trainable=True
)
class MyPolicy(Policy):
    def __init__(
            self,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            featurizer: Optional[TrackerFeaturizer] = None,
            **kwargs: Any,
        ) -> None:
            super().__init__(
            config, model_storage, resource, execution_context, featurizer, **kwargs
            )
            
    def train(
        self,
        training_trackers: List[TrackerWithCachedStates],
        domain: Domain,
        precomputations: Optional[MessageContainerForCoreFeaturization] = None,
    ) -> Resource:
        pass

    def predict_action_probabilities(
        self,
        tracker: DialogueStateTracker,
        domain: Domain,
        precomputations: Optional[MessageContainerForCoreFeaturization] = None,
        rule_only_data: Optional[Dict[Text, Any]] = None,
        **kwargs: Any,
    ) -> PolicyPrediction:
        # The code below offers a way to set the Beam Custom action which allows for intents that are 
        # not the top probability to be set and expanded upon
        # set the values for all the confidence of actions to 0 
        confidences = list(np.zeros(domain.num_actions))
        # make the prediction alwways set to beam action because then it will choose the next best one 
        confidences[domain.index_for_action(ACTION_BEAM)] = 1.0
        print(tracker.latest_message)
        print("Actions", tracker.latest_action_name)
        print("INTENT:", tracker.intent_ranking)

        return self._prediction(confidences)


    '''
    The code below is the theory behind the multi turn beam search between intent and action. 
    There are some values that need to be consulted on if they are possible to retrieve through a custom policy. 

    '''
    # last_user_uttered_event = tracker.get_last_event_for(UserUttered)
    # last_bot_uttered_event = tracker.get_last_event_for(BotUttered)

    # k = 5 
    # while the intent is not goodbye:
    #     #everyime step being an action or intent event 
    #     for each event occuring: 
    #         #for every thread 
    #         #keeping track of the thread probabilities through summing the probabilities of each event
    #         score = list(np.zeros(k))
    #         for t in range k : 
    #             if tracker.latest_message == last_user_uttered_event:
    #                 #gives a list of all possible intents and their confidence levels ordred from most to least probable 
    #                 intent_ranking = tracker.last_user_uttered_event['intent_ranking']
    #                 #keep only the top k rankings 
    #                 intent_ranking = intent_ranking[:k]
    #                 intentName = intent_ranking[t].get('name')
    #                 intentConfidence = intent_ranking[t].get('confidence')
    #                 # set the user event with the intent for current thread and moves to the next event
    #                 UserUttered(tracker.last_user_uttered_event['name']{"intent": {'name': intentName , 'confidence': intentConfidence}})]
    #                 #add to final score at correct index 
    #                 score[t] += intentConfidence
    #             if tracker.latest_message == last_bot_uttered_event:
    #                 #gives a list of all possible intents and their confidence levels ordred from most to least probable 
    #                 action_ranking = tracker.last_bot_uttered_event['action_ranking']
    #                 #keep only the top k 
    #                 action_ranking = action_ranking[:k]
    #                 actionName = action_ranking[t].get('name')
    #                 actionProb = action_ranking[t].get('probability')
    #                 # set the user event with the intent for current thread and moves to the next event
    #                 BotUttered(tracker.last_bot_uttered_event['name']{"action": {'name': actionName , 'probability': actionProb}})]
    #                 #add to final score at correct index 
    #                 score[t] += actionProb
    
    #     finalThread = argmax(score)


          

@classmethod
def _metadata_filename(cls):
    return "beam_policy_files.json"

def _metadata(self):
    return{
        "priority": self.priority
    }