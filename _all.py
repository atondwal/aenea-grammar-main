# _all.py: main rule for DWK's grammar

try:
    from aenea import *
except:
    from dragonfly import *

import keyboard
import words
import programs

from dragonfly.log import setup_log
setup_log()

release = Key("shift:up, ctrl:up, alt:up")

alternatives = []
alternatives.append(RuleRef(rule=keyboard.KeystrokeRule()))
alternatives.append(RuleRef(rule=words.FormatRule()))
alternatives.append(RuleRef(rule=words.ReFormatRule()))
alternatives.append(RuleRef(rule=words.NopeFormatRule()))
alternatives.append(RuleRef(rule=words.PhraseFormatRule()))
alternatives.append(RuleRef(rule=programs.ProgramsRule()))
root_action = Alternative(alternatives, name="altern")

sequence = Repetition(root_action, min=1, max=4, name="sequence")

class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence,  # Sequence of actions defined above.
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        count = extras["n"]  # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()
            release.execute()

class AlternativeRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    altern = root_action
    spec = "<altern> [[[and] repeat [that]] <n> times]"
    extras = [
        altern,
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        count = extras["n"]  # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()
            release.execute()


# Load engine before instantiating rules/grammars!
# Set any configuration options here as keyword arguments.
engine = get_engine("kaldi",
    model_dir='kaldi_model_zamia',
    # tmp_dir='kaldi_tmp',  # default for temporary directory
    # vad_aggressiveness=3,  # default aggressiveness of VAD
    # vad_padding_ms=300,  # default ms of required silence surrounding VAD
    # input_device_index=None,  # set to an int to choose a non-default microphone
    # cloud_dictation=None,  # set to 'gcloud' to use cloud dictation
    auto_add_to_user_lexicon=True,
)
# Call connect() now that the engine configuration is set.
engine.connect()

grammar = Grammar("root rule")
grammar.add_rule(RepeatRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.
print("Listening...")
engine.do_recognition()
