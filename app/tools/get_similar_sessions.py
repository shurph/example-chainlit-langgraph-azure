from langchain_core.tools import tool


@tool
def get_similar_sessions(topic):
    """

    Use this function to get a list of sessions that are potentially relevant for the specified topic.
    The sessions are provided in the format of `id|title|abstract|speakers|city|start-time|end-time`.

    """
    return """001|Advances in AI Research|A deep dive into the latest AI advancements and their applications.|Dr. Jane Smith|NYC|2025-06-10T10:00:00|2025-06-10T11:00:00
002|Ethics in Machine Learning|Discussion on ethical dilemmas in ML deployments.|Prof. Alan Doe|Berezino|2025-06-10T11:30:00|2025-06-10T12:30:00
003|Neural Networks for Beginners|Introductory session on how neural networks work.|Dr. Emily Tan|Berezino|2025-06-10T13:00:00|2025-06-10T14:00:00
004|Future of Quantum Computing|Exploring how quantum technologies will reshape computing in the next decade.|Dr. Max Lee|NYC|2025-06-10T14:30:00|2025-06-10T15:30:00
005|Design Thinking in Tech|Learn how to apply design thinking principles to build user-centric products.|Anna Petrova|Moscow|2025-06-10T16:00:00|2025-06-10T17:00:00
006|Cybersecurity Trends 2025|Review of the top threats and protection strategies in cybersecurity.|Michael Chen|Kazan|2025-06-11T09:00:00|2025-06-11T10:00:00
007|Building Scalable Microservices|Best practices for designing and maintaining scalable microservices architecture.|Sarah Khan|San Francisco|2025-06-11T10:30:00|2025-06-11T11:30:00
008|AI in Healthcare|Case studies on how AI is transforming diagnostics and treatment.|Dr. Ahmed Saleh|Warsaw|2025-06-11T12:00:00|2025-06-11T13:00:00
009|Blockchain Beyond Crypto|Discover how blockchain is being applied outside of cryptocurrency.|Elena Morozova|Berlin|2025-06-11T13:30:00|2025-06-11T14:30:00
010|Inclusive Product Development|Creating products that serve diverse users and promote accessibility.|Tariq Johnson|New York City|2025-06-11T15:00:00|2025-06-11T16:00:00
011|Deep Reinforcement Learning|Dive into algorithms and real-world uses of reinforcement learning.|Prof. Li Wei|Paris|2025-06-12T09:00:00|2025-06-12T10:00:00
012|Serverless Architecture Demystified|Pros, cons, and practical tips for serverless infrastructure.|Nina Kuznetsova|Moscow|2025-06-12T10:30:00|2025-06-12T11:30:00
013|Tech & Climate Change|How emerging technologies are tackling environmental challenges.|Carlos Mendes|Mexico City|2025-06-12T12:00:00|2025-06-12T13:00:00
014|Mental Health in Tech|Strategies to maintain well-being in high-stress tech environments.|Rachel Kim|San Francisco|2025-06-12T13:30:00|2025-06-12T14:30:00
015|The Art of Code Reviews|Techniques for effective, respectful, and helpful code reviews.|Igor Petrov|Saint Petersburg|2025-06-12T15:00:00|2025-06-12T16:00:00
016|Women in STEM Leadership|Panel on breaking barriers and leading innovation.|Panel: Dr. Laura Singh, Amara Okafor|Minsk|2025-06-12T16:30:00|2025-06-12T17:30:00
017|ML Ops in Practice|Deploying and maintaining machine learning models in production.|Viktor Ivanov|Paris|2025-06-13T09:00:00|2025-06-13T10:00:00
018|How to Pitch a Tech Startup|Insights on crafting a compelling pitch for investors.|Jasmine Ortega|Almaty|2025-06-13T10:30:00|2025-06-13T11:30:00"""
