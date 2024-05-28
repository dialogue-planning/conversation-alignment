# Dialogue Planning

This project is part of an ongoing [Dialogue Planning Initiative](https://github.com/dialogue-planning).

# Dialogue Agent Conversation Alignment

Published to CAI 2024 by Rebecca De Venezia, Natalie Nova, and Christian Muise.

Task-oriented dialogue agents have been growing at an extraordinarily fast pace, especially within business-oriented settings. 
Verification is a core component of any task-oriented dialogue agent, as it is crucial for a variety of conversations to be handled predictably.
The current approaches used to analyze agent capabilities are time-consuming and tedious, leaving dialogue designers unable reliably understand the conversational capabilities of their agents. 
With this project, we propose to address this issue through a method for conversation alignment. 
We achieve this using a tailored beam search algorithm to explore how well the agent can handle given conversation examples.
Our method builds on the viewpoint of dialogue agent creation as a planning process, and we leverage both learning and planning techniques to achieve conversation alignment. 
We demonstrate that beam search is effective at identifying conversations that are problematic for the agent, and our work opens the door to streamlined testing for task-oriented dialogue agents.

## Installation
Run `pip install -r requirements.txt` and follow the instructions to install graphviz [here](https://graphviz.org/download/).

Please see our API Documentation [here](https://dialogue-planning.github.io/conversation-alignment/).
