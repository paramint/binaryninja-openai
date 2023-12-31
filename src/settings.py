import json
from binaryninja.settings import Settings
from . exceptions import RegisterSettingsGroupException, \
                         RegisterSettingsKeyException

class OpenAISettings(Settings):

    def __init__(self) -> None:
        # Initialize the settings with the default instance ID.
        super().__init__(instance_id='default')
        # Register the OpenAI group.
        if not self.register_group('openai', 'OpenAI'):
            raise RegisterSettingsGroupException('Failed to register OpenAI '
                                                 'settings group.')
        # Register the setting for the API key.
        if not self.register_api_key_settings():
            raise RegisterSettingsKeyException('Failed to register OpenAI API '
                                               'key settings.')

        # Register the setting for the model used to query.
        if not self.register_model_settings():
            raise RegisterSettingsKeyException('Failed to register OpenAI '
                                               'model settings.')

        # Register the setting for the max tokens used for both the prompt and
        # completion.
        if not self.register_max_tokens():
            raise RegisterSettingsKeyException('Failed to register OpenAI '
                                               'max tokens settings.')

    def register_api_key_settings(self) -> bool:
        '''Register the OpenAI API key settings in Binary Ninja.'''
        # Set the attributes of the settings. Refer to:
        # https://api.binary.ninja/binaryninja.settings-module.html
        properties = {
            'title': 'OpenAI API Key',
            'type': 'string',
            'description': 'The user\'s OpenAI API key used to make requests '
            'the server.'
        }
        return self.register_setting('openai.api_key', json.dumps(properties))

    def register_model_settings(self) -> bool:
        '''Register the OpenAI model settings in Binary Ninja.
        Defaults to gpt-3.5-turbo.
        '''
        # Set the attributes of the settings. Refer to:
        # https://api.binary.ninja/binaryninja.settings-module.html
        properties = {
            'title': 'OpenAI Model',
            'type': 'string',
            'description': 'The OpenAI model used to generate the response.',
            # https://beta.openai.com/docs/models
            'enum': [
                'gpt-4',
                'gpt-4-32k',
                'gpt-3.5-turbo',
                'text-davinci-003',
                'text-davinci-002',
                'text-curie-001',
                'text-babbage-001',
                'text-babbage-002',
                'code-davinci-002',
                'code-cushman-001'
            ],
            'enumDescriptions': [
                'More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration.',
                'Same capabilities as the base gpt-4 mode but with 4x the context length. Will be updated with our latest model iteration.',
                'Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.',
                'Can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models.',
                'Similar capabilities to text-davinci-003 but trained with supervised fine-tuning instead of reinforcement learning'
                'Very capable, but faster and lower cost than Davinci.',
                'Capable of straightforward tasks, very fast, and lower cost.',
                'Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.',
                'Most capable Codex model. Particularly good at translating natural language to code. In addition to completing code, also supports inserting completions within code.',
                'Almost as capable as Davinci Codex, but slightly faster. This speed advantage may make it preferable for real-time applications.'
            ],
            'default': 'gpt-3.5-turbo'
        }
        return self.register_setting('openai.model', json.dumps(properties))

    def register_max_tokens(self) -> bool:
        '''Register the OpenAI max tokens used for both the prompt and
        completion. Defaults to 2,048. The Davinci model can use 4,000 or 8,000
        tokens for GPT and Codex respectively. Check out the documentation here:
        https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        '''

        properties = {
            'title': 'OpenAI Max Completion Tokens',
            'type': 'number',
            'description': 'The maximum number of tokens used for completion. Tokens do not necessarily align with word or instruction count. Typically, each token is four characters. If your function is very large, you may need to decrease this value, as the number of tokens in your prompt counts against the total number of tokens supported by the model. Not all models support the same number of maximum tokens; most support 2,048 tokens. For larger functions, check out text-davinci-003 and code-davinci-002 which support 4,000 and 8,000 respectively. For the maximum amount of tokens, check out gpt-4-32k which supports up to 32,768 tokens. This may be costly, however.',
            'default': 1_024,
            'minValue': 1,
            'maxValue': 32_768,
            'message': "Min: 1, Max: 32,768"
        }
        return self.register_setting('openai.max_tokens',
                                     json.dumps(properties))
