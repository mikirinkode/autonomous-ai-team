class Agent:
    def __init__(self, agent_name, agent_skills, openai_client, openai_model):
        self.name = agent_name
        self.skills = agent_skills
        self.memories = [
            {"role": "system", "content": agent_skills}
        ]
        self.openai_client = openai_client
        self.openai_model = openai_model
        
    def chat(self, prompt):
        self.memories.append({"role": "user", "content": prompt})
        result = self.openai_client.chat.completions.create(
            model = self.openai_model,
            messages= self.memories,
            stream=True,
        )
        return result