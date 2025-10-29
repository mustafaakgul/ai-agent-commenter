# Product::AI Agent Commenter
* Description: An AI-powered agent that analyzes and generates meaningful comments based on content context

## To Run Application
* Local:
  * Add and Set Up Python Interpreter in Settings
  * python3 -m venv .venv
  * source .venv/bin/activate
  * which python
  * python -version
  * pip install -r requirements.txt (pip freeze > requirements.txt)
  * python manage.py makemigrations
  * python manage.py migrate
  * python manage.py collectstatic
  * python manage.py createsuperuser, Test(admin-admin)
  * ipconfig getifaddr en0 1
  * python manage.py runserver 192.168.1.11:8000
* Dev: Heroku
* Production: Domain and Allowed Host, Debug False, Hide Secret Key, https://docs.djangoproject.com/en/5.2/howto/deployment/, https://github.com/heroku/python-getting-started/blob/main/gettingstarted/settings.py

## Technology Stack
* Python, Django and FastAPI Technologies: Development
* Figma: Design and Project Development
* Postman, DRF UI, Swagger: API Observation
* PyCharm: IDE
* Slack: Team Communication, Project Management, Collaboration, Notification

## Features
* DB Storage: Stores comments and generated responses
* Context Understanding: Analyzes the emotional tone and topic of the comment
* Quality Check: Ensures professionalism and appropriateness
* API/scraper that fetches product reviews
* System that categorizes comment data (positive/negative/neutral), sentiment

## Technology Stack To Be Added
* Hugging Face

## Features To Be Added
* Personalization: Adapts to match the brand's voice
* Product tables, product based response generation
* Memory: To remember past comments and responses, LLM bypass, ragging
* Prompt Templates, Tools: Custom templates for different types of comments, selects appropriate response template based on the situation
* Chains: Comment analysis → response generation → quality-control chain
* Agents: To manage different scenarios
* Comment sentiment analysis
* Customized responses based on product features
* Escalation for complaint cases
* Tone adjustments to match the brand's voice
* Comment analysis - sentiment, category, urgency analysis
* Web interface (Streamlit, Flask) 
* More advanced sentiment analysis 
* Multilingual support 
* Automatic spam filtering 
* Comment scoring system
* Visual reporting 
* Industry-specific templates
* Prompt Templates: Predefined and optimized prompts help you ask the language model more accurate and context-appropriate questions.
* Context Management: The system can produce more meaningful responses by taking conversation history or the results of previous prompts into account. This is important for chatbots or multi-step queries.
* History Awareness: The chain shapes future steps by using information obtained from earlier steps. It is ideal for methods like retrieval-augmented generation (RAG). RAG enables verification of the language model's responses against data sources.
* Automatic generation of product descriptions

### Technical Info
* LLM Models
  * OpenAI
  * Gemini
  * Claude
  * Deepseek
  * Llama
* AI Agent Frameworks - Agentic Frameworks
  * CrewAI - 30k, Python
  * LangChain - 100k, Python, Ragging, Vector DBs, 700+ Integrations
  * Swarm - 20k, Python
  * Agno - 24k, Python
  * Openai Agents - 8k, Python
  * LangGraph - 11k, Python
  * LlamaIndex - 40k, Python
  * Semantic Kernel - 28k, C#
  * Langflow - 54k, Python
  * AutoGen - 43k, Python
  * MetaGPT - 54k, Python
  * n8n - 74k, Ts
  * browser-use - 53k, Python
  * composio 25k - AI Agent & Tooling
* AI Workflows
  * https://github.com/langgenius/dify
  * https://github.com/n8n-io/n8n
  * https://github.com/langflow-ai/langflow
  * https://github.com/apache/airflow
  * https://github.com/labring/FastGPT
  * https://github.com/Avaiga/taipy
  * https://github.com/eosphoros-ai/DB-GPT
* Agents:
  * https://getstream.io/blog/multiagent-ai-frameworks/
  * https://github.com/kyrolabs/awesome-agents
  * https://github.com/e2b-dev/awesome-ai-agents
  * https://github.com/Jenqyang/Awesome-AI-Agents
  * https://github.com/browser-use/browser-use
  * https://www.pageon.ai/blog/ai-agent-github
* MCP Server
  * https://github.com/modelcontextprotocol
  * https://cursor.directory/mcp
  * https://docs.cursor.com/context/model-context-protocol
  * https://modelcontextprotocol.io/introduction
  * https://docs.anthropic.com/en/docs/agents-and-tools/mcp
  * https://github.com/topics/mcp-server
  * https://github.com/punkpeye/awesome-mcp-servers
  * https://github.com/wong2/awesome-mcp-servers
  * https://github.com/MobinX/awesome-mcp-list
  * MCV Server List: https://smithery.ai/?q=twitter
  * To Add MCV Server (npx -y @smithery/cli@latest install @nickclyde/duckduckgo-mcp-server --client claude --key 0e021ec0-0c65-4b37-a239-a037f46b081f)
  * To Add Developed MCV Server (Claude Desktop > Settings > Developer > Edit Config > Edit claude_desktop_config.json)
* AI Agent Framework Info:
  * https://medium.com/@vipra_singh/ai-agents-frameworks-part-3-ca8ce33c2f35
  * https://www.marketermilk.com/blog/best-ai-agent-platforms
  * https://www.linkedin.com/pulse/top-5-ai-agent-platforms-you-should-know-2025-edition-jadeja-aw77f/
  * https://botpress.com/blog/ai-agent-frameworks
  * https://www.shakudo.io/blog/top-9-ai-agent-frameworks
  * https://research.aimultiple.com/open-source-ai-agents/
  * https://hub.athina.ai/top-5-open-source-frameworks-for-building-ai-agents-with-examples/
  * https://medium.com/@aydinKerem/which-ai-agent-framework-i-should-use-crewai-langgraph-majestic-one-and-pure-code-e16a6e4d9252
  * https://lekha-bhan88.medium.com/top-5-agentic-ai-frameworks-to-watch-in-2025-9d51b2b652c0
  * https://medium.com/@vipra_singh/ai-agents-frameworks-part-3-ca8ce33c2f35
* AI Agent Info:
  * https://github.com/e2b-dev/awesome-ai-agents
  * https://github.com/Jenqyang/Awesome-AI-Agents
  * https://research.aimultiple.com/open-source-ai-agents/
  * https://github.com/SamurAIGPT/Best-AI-Agents
  * https://medium.com/@springs_apps/open-source-ai-agents-how-to-use-them-and-best-examples-e19560280df1
  * https://github.com/Significant-Gravitas/AutoGPT 174k, Python
* AI Agent Workflow Info
  * https://dev.to/fast/5-open-source-projects-that-will-transform-your-ai-workflow-190g
  * https://medium.com/@vipra_singh/ai-agent-workflow-vs-agent-part-5-2026a890a33d
  * https://medium.com/@nhshinwari21/transform-your-work-processes-instantly-with-these-9-no-code-and-ai-workflow-wonders-7b5c65eaa626
