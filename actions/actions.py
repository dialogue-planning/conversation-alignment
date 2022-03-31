# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from collections import ChainMap

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUttered, ActionExecuted, BotUttered, ActionReverted
from rasa_sdk.events import SlotSet

class ActionHelloWorld(Action):
    #actionNext = next_action
    #print("Action", actionNext)

    def name(self) -> Text:
        return "action_hello_world"
            
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #print("Intially", tracker.latest_message)
        intent_ranking = tracker.latest_message['intent_ranking']
        print("INTENT", intent_ranking)


        bot_event = next(e for e in reversed(tracker.events) if e["event"] == "bot")
        #print("Action", bot_event)
        reverting = ActionReverted()
        #print("FIRST VALUE", intent_ranking[0])
        beamList = []
        confidenceRank = []
        intent_ranking = intent_ranking[:3]
        for i in range(len(intent_ranking)): 
            #print(intent_ranking[i])
            #print("Dictionary Name: ", intent_ranking[i].get('name'))
            beam = intent_ranking[i].get('name')
            beamConfidence = intent_ranking[i].get('confidence')
            beamList.append(beam)
            confidenceRank.append(beamConfidence)
            
            print("BEAM SEARCHER: ", beamList)

        #print("Post", event)
        #intentTime = tracker.latest_message['intent_ranking']
        #print("INTENT", intentTime)
        return [ActionExecuted("action_listen")] + [UserUttered("/beam_intent", {"intent": {'name': beamList[1] , 'confidence': 1.0}})]

        # Expanding the beam search means we start with the new intent all over again 
        #return self.newIntent(beamThree, tracker)
        #return 

class ActionSearchResraurant(Action):
    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            dispatcher.utter_message(text="Ok! I am searching restaurants for you")

class ActionGetDetails(Action):
    def name(self) -> Text:
        return "action_getDetails"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent_ranking = tracker.latest_message['intent_ranking']
        print(intent_ranking)
        #print("RESPONSE", tracker.latest_message.get("response_selector"))
        return ()

        
class ActionSearchConcerts(Action):
    def name(self):
        return "action_search_concerts"

    def run(self, dispatcher, tracker, domain):
        concerts = [
            {"artist": "Foo Fighters", "reviews": 4.5},
            {"artist": "Katy Perry", "reviews": 5.0},
        ]
        description = ", ".join([c["artist"] for c in concerts])
        dispatcher.utter_message(text=f"{description}")
        return [SlotSet("concerts", concerts)]


class ActionSearchVenues(Action):
    def name(self):
        return "action_search_venues"

    def run(self, dispatcher, tracker, domain):
        venues = [
            {"name": "Big Arena", "reviews": 4.5},
            {"name": "Rock Cellar", "reviews": 5.0},
        ]
        dispatcher.utter_message(text="here are some venues I found")
        description = ", ".join([c["name"] for c in venues])
        dispatcher.utter_message(text=f"{description}")
        return [SlotSet("venues", venues)]


class ActionShowConcertReviews(Action):
    def name(self):
        return "action_show_concert_reviews"

    def run(self, dispatcher, tracker, domain):
        concerts = tracker.get_slot("concerts")
        dispatcher.utter_message(text=f"concerts from slots: {concerts}")
        return []


class ActionShowVenueReviews(Action):
    def name(self):
        return "action_show_venue_reviews"

    def run(self, dispatcher, tracker, domain):
        venues = tracker.get_slot("venues")
        dispatcher.utter_message(text=f"venues from slots: {venues}")
        return []


class ActionSetMusicPreference(Action):
    def name(self):
        return "action_set_music_preference"

    def run(self, dispatcher, tracker, domain):
        """Sets the slot 'likes_music' to true/false dependent on whether the user
        likes music"""
        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirm":
            return [SlotSet("likes_music", True)]
        elif intent == "deny":
            return [SlotSet("likes_music", False)]
        return []