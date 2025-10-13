from integrations.ai.agents.agent_comment.llm import claude


def create(id: int, content: str):
    claude.execute(id, content)
