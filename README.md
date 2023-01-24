# Dialogue Agent Conversation Alignment

This is Natalie Nova's undergraduate Thesis project code continued, with contributions from Rebecca De Venezia.

Task-oriented dialogue agents have been growing at an extraordinarily fast pace, especially within business-oriented settings. 
Verification is a core component of any task-oriented dialogue agent, as it is crucial for a variety of conversations to be handled predictably.
The current approaches used to analyze agent capabilities are time-consuming and tedious, leaving dialogue designers unable reliably understand the conversational capabilities of their agents. 
With this project, we propose to address this issue through a method for conversation alignment. 
We achieve this using a tailored beam search algorithm to explore how well the agent can handle given conversation examples.
Our method builds on the viewpoint of dialogue agent creation as a planning process, and we leverage both learning and planning techniques to achieve conversation alignment. 
We demonstrate that beam search is effective at identifying conversations that are problematic for the agent, and our work opens the door to streamlined testing for task-oriented dialogue agents.

For beam search Installation and Usage instructions, as well as API documentation, please see our [docs website](https://dialogue-planning.github.io/conversation-alignment/).
