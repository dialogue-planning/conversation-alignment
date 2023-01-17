.. Conversation Alignment documentation master file, created by
   sphinx-quickstart on Mon Jan  9 10:28:03 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Conversation Alignment's documentation!
==================================================
.. autosummary::
   :toctree: generated
   :recursive:

   beam_search

Task-oriented dialogue agents have been growing at an extraordinarily fast pace, especially within business-oriented settings. 
Verification is a core component of any task-oriented dialogue agent, as it is crucial for a variety of conversations to be handled predictably.
The current approaches used to analyze agent capabilities are time-consuming and tedious, leaving dialogue designers unable reliably understand the conversational capabilities of their agents. 
With this project, we propose to address this issue through a method for conversation alignment. 
We achieve this using a tailored beam search algorithm to explore how well the agent can handle given conversation examples.
Our method builds on the viewpoint of dialogue agent creation as a planning process, and we leverage both learning and planning techniques to achieve conversation alignment. 
We demonstrate that beam search is effective at identifying conversations that are problematic for the agent, and our work opens the door to streamlined testing for task-oriented dialogue agents.

To get started with implementing beam search in your own dialogue-as-planning agents, you will want to clone this repository and implement the abstract methods in :py:func:`beam_srch_data_structs <beam_search.beam_srch_data_structs>`.

**Please note that Python >= 3.7 is required.**

Then, running a beam search is as easy as follows:

.. code-block:: python

   from beam_search.beam_search_core import BeamSearchExecutor

   conversation = [
                    {"AGENT": "Hi!"},
                    {"USER": "Hello."}
                ]

   gen = BeamSearchExecutor(3, 1, conversation, True, "graph_file", param=rollout_param)
   gen.beam_search()

   # changing the settings and running again
   gen.k = 5
   gen.max_fallbacks = 2
   gen.graph_file = "another_graph_file"
   gen.beam_search()