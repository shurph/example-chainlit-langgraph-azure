import chainlit as cl

starters = [
    cl.Starter(
        label="Example 1: smoothies + STEM",
        message="I love smoothies and I'm into STEM. What would you recommend for me?",
        icon="/public/icons/cup-soda.svg",
    ),
    cl.Starter(
        label="Example 2: coffee + STEM",
        message="I'm a coffee lover and I like STEM. What can you propose to me?",
        icon="/public/icons/coffee.svg",
    ),
    cl.Starter(
        label="Example 3: coffee + STEM + Gdansk",
        message="I'm a coffee lover and interested in STEM. I'm currently in Gdańsk, Poland, and I'd like to attend a conference. However, the weather is important to me. What can you suggest?",
        icon="/public/icons/house.svg",
    ),
    cl.Starter(
        label="Example 4: weather in Berezino",
        message="What's the weather in Berezino?",
        icon="/public/icons/idea.svg",
    ),
    cl.Starter(
        label="Example 5: weather in Moscow",
        message="What's the weather in Moscow?",
        icon="/public/icons/idea.svg",
    ),
    cl.Starter(
        label="Example 6: weather in Minsk",
        message="What's the weather in Minsk?",
        icon="/public/icons/idea.svg",
        # Example:
        # Question: What's the weather in Minsk?
        # Answer:
        # I currently do not have the weather information for Minsk. However, I can provide weather details for Berezino, which is located in Belarus, or for other major cities like Moscow or Paris. Let me know if you'd like me to proceed!
    ),
]
