from deepl_assistant import DeepLAssistant

input("Are you using a VPN?\n")

assistant = DeepLAssistant()

assistant.start_driver()
assistant.set_deepl_languages()

# then use -i
# remember to quit driver
