from __future__ import annotations
from typing import List, Dict, Text, Optional, Any, Union, Tuple

from rasa.core.policies.policy import PolicyPrediction, Policy
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.engine.storage.resource import Resource
from rasa.shared.core.domain import Domain
from rasa.core.constants import DEFAULT_POLICY_PRIORITY
from rasa.shared.core.constants import ACTION_LISTEN_NAME
from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from datetime import time, datetime

from rasa.engine.recipes.default_recipe import DefaultV1Recipe

TIME_FORMAT = "%I:%M %p"

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=True
)


class MyPolicy(Policy):
    
    def get_default_config() -> Dict[Text, Any]:
        return {"key1": "value1"}
    def __init__(
        self,
        featurizer: Optional[TrackerFeaturizer]= None, 
        priority: int = 2,
        **kwargs: Any,

        ) -> None:
        super().__init__(priority=priority,**kwargs)


    def train(
        self,
        training_trackers: List[TrackerWithCachedStates],
        domain: Domain,
        #interpreter: NaturalLanguageInterpreter,
        **kwargs: Any,
    ) -> Resource: 
        "This policy is not influenced by stories so we dont need any training "
        pass 
    
    def predict_action_probabilities(
        self,
        tracker: DialogueStateTracker,
        domain: Domain,
        #interpreter: NaturalLanguageInterpreter,
        **kwargs: Any,
        ) -> PolicyPrediction: 
        """This is wher the magic happen and we make our prediction of what the next action should be"""
        
        pass 

    @classmethod
    def _metadata_filename(cls):
        pass
    
    def _metadata(self):
        pass