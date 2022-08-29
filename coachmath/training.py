# MIT License
#
# Copyright (c) 2022 Manuel Proissl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Main training class for Jupyter Notebooks."""

# Dependencies
from datetime import datetime as _dt
from IPython.display import display, HTML
from google_trans_new import google_translator as translator
from importlib import import_module as _import
from time import sleep
import json


class Training():
    """Simple training class for basic math problems."""
    def __init__(self,
                 who: str,
                 study_id: str = None,
                 study_params: dict = None,
                 repetitions: int = 1,
                 language: str = "de",
                 translate: bool = True,
                 max_tasks: int = -1):
        """Init a new training.

        Args:
            who: Name of student
            study_id: (Optional) Identifier of study to load
            study_params: (Optional) Parameters for task (method)
            repetitions: (Optional) Number of task repetitions
            language: (Optional) Default display language
            translate: (Optional) Translate into default language
            max_tasks: (Optional) Limit number of tasks
        """
        # Init by args
        self.who = who
        self.study_id = study_id
        self.study_params = study_params
        self.repetitions = repetitions
        self.language = language
        self.translate = translate
        self.translator = translator()
        self.max_tasks = max_tasks

        # Init defaults
        self.start_dt = None
        self.end_dt = None
        self.tasks = []
        self.report = {}

        # Launch
        self.start()

    def start(self):
        # Say Hi
        self._display(f"Hello {self.who} :)")

        # Select
        self._select()

        # Run
        self._run(self.study_id)

        # Show results
        self._eval()

        # Save
        self._save()
    
    def _select(self):
        if self.study_id is None:
            self._display("What do you want to learn?")
            try:
                self.study_id = str(self._display(self._studies(), user_input=True, html_tag="strong"))
            except Exception as err:
                self._display("Try again.")
                self._select()
        
        if self.study_id not in self._study_directory():
            self._select()

    def _studies(self) -> str:
        li = "".join([f"<li>[{k}]: {n['desc']}</li>" for k,n in self._study_directory().items()])
        return f"<ul>{li}</ul>"
    
    def _study_directory(self, study_id: str = None):
        directory = {
            "1": {
                "desc": "Multiplication up to 100",
                "path": "coachmath.tasks.multiplication",
                "task": "basic_integer_multiplication",
                "default_params": {
                    "max_product": 100,
                    "max_tasks": self.max_tasks
                }
            },
            "2": {
                "desc": "Division up to 100",
                "path": "coachmath.tasks.multiplication", # TODO
                "task": "basic_integer_multiplication",  # TODO
            }
        }
        if study_id is not None:
            return directory[study_id]
        else:
            return directory
    
    def _run(self, option):
        # Start
        self.start_dt = _dt.now()

        # Load
        config = self._study_directory[self.study_id]
        _method = getattr(_import(config["path"]), config["task"])
        print(method)
        self.tasks = _method(**config["default_params"])

        # Start tasks
        for n_iter in range(1, self.repetitions+1):
            for task_idx, task in enumerate(self.tasks):

                # Present
                self._display(f"Task {task_idx+1} (Round {n_iter})")
                self._display("<hr>", skip_translate=True)
                self.tasks[task_idx]["start_dt"] = _dt.now()
                try:
                    self.tasks[task_idx]["answer"] = int(self._display(task["task"], user_input=True, html_tag="h3"))
                except Exception:
                    self.tasks[task_idx]["answer"] = None
                    pass
                self.tasks[task_idx]["end_dt"] = _dt.now()

                # Process
                self.tasks[task_idx]["correct"] = (self.tasks[task_idx]["result"] == self.tasks[task_idx]["answer"])
                self.tasks[task_idx]["duration"] = (self.tasks[task_idx]["end_dt"] - self.tasks[task_idx]["start_dt"]).seconds

        # End
        self.end_dt = _dt.now()

    def _eval(self):
        self._display("<hr>", skip_translate=True)
        self._display("Results")
        self._display("<br/>", skip_translate=True)

        # Number of completed tasks
        l = len(self.tasks)
        self.report[self._get_text("Completed Tasks")] = l

        # Number of correct answers
        c = sum([ task["correct"] for task in self.tasks ])
        self.report[self._get_text("Correct Answers")] = c

        # Percentage of correct answers
        p = int(( c/l ) * 100)
        self.report[self._get_text("Percentage Correct")] = p

        # Grade (Swiss system)
        g = round(6.0 * (p/100), 1)
        self.report[self._get_text("Grade")] = g if g > 1 else 1.0

        # Total time
        t = int((self.end_dt - self.start_dt).seconds / 60)
        self.report[self._get_text("Duration to Complete (Minutes)")] = t

        # Time for tasks
        tt = [ (task["end_dt"] - task["start_dt"]).seconds for task in self.tasks ]
        self.report[self._get_text("Fastest Time to Answer (Seconds)")] = min(tt)
        self.report[self._get_text("Slowest Time to Answer (Seconds)")] = max(tt)
        self.report[self._get_text("Average Time Answer (Seconds)")] = int(sum(tt)/len(tt))

        # Display
        _show = "<ul>"
        for item in self.report:
            _show += f"<li><strong>{item}:</strong> {self.report[item]}</li>"
            _show += "</ul>"
        self._display(_show, html_tag= "p")

    def _display(self,
                 msg: str,
                 user_input: bool = False,
                 html_tag: str = "h1",
                 skip_translate = False) -> any:
        
        display(HTML('<{}>{}</{}>'.format(html_tag,
                                          self._get_text(msg, skip_translate),
                                          html_tag)))
        if user_input:
            return input()
        else:
            return None
    
    def _get_text(self, msg: str, skip_translate: bool = False) -> str:
        if (self.language != "en" or self.translate or not skip_translate):
            try:
                return _translator.translate(msg, lang_tgt=self.language)
            except Exception:
                self.translate = False
                pass
        
        return msg
    
    def _save(self):
        export_dt = _dt.now()
        export = {
            "timestamp": _dt.timestamp(export_dt),
            "datetime:": export_dt.strftime("%Y%m%d%H%M"),
            "who": self.who,
            "study_id": self.study_id,
            "study_name": self._study_directory(self.study_id),
            "repetitions": self.repetitions,
            "report": self.report
        }
        with open(f"{self.study_id}_{export['datetime']}.json", "w") as _file:
            json.dump(export, _file, indent=4)
