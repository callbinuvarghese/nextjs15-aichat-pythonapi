# nextjs15-aichat-pythonapi

A chatbot in NextJS 15 ShadCN Chat UI. It calls python backend locally which in turn calls the LLM providing serverside filtering

The Shad Chatbot UI is modified to display HTML response from the server to facilitate function calling HTML response to be rendered in Chat response.

NextJS15 Shad CN does not directly call LLMs. It has a server component in python that calls the LLM and the chatbot interact with the python server which in turn calls the LLMs and also perform function calling
