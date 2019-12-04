# Circle game, a Metacognitive Task

This is a beta version of an experiment equivalent to the one used by [Salles et al](http://www.sciencedirect.com/science/article/pii/S0885201416301538).
The circle game consists of:
The type I task, a perceptual task which consists in identifying the largest among 9 black circles of varying size. Followed by,
the type II task which involves a conﬁdence judgment produced by the participants.
If you use it pleas cite [1].

The main difference with the original experiment is that in this new and improved version, we use a Staircase procedure instead of a Quest one.
We have made this modification to the original version in order to achieve a more satable level of performance. The default parameters of the Staircase are nUp=1 and nDown=3 which yields a 0.82 average value of performance.

[1] Salles, A., Ais, J., Semelman, M., Sigman, M., & Calero, C. I. (2016). The metacognitive abilities of children and adults. Cognitive Development, 40, 101-110.


## Installation

In order to use this task you must have the PsychoPy (a platform-independent experimental control system written in the Python interpreted language which uses entirely free libraries) already installed. If you don't have it please go to the [installation page](http://www.psychopy.org/installation.html) and follow the instructions.

First, you have to download this repository and unzip it some where on your pc.
You can also clone this repo, if you find that useful.


Once you have the PsychoPy installed, run PsychoPy and open the circles.psyexp file.


## Settings

There are nine types of trials:
* PLAIN. Only a Type I task is presented to the participant. The screen will display the circles and wait for a response. No additional Type II task will be presented.

* SLIDER. First, a Type I task is presented, the screen will display the circles, wait for a response and then, the participant’s confidence level is inquired through a slider.

* WAGE. First, a Type I task is presented, the screen will display the circles, wait for a response and then, the participant’s confidence level is inquired through a Green Tick or a Red Cross button.
Participants were told to choose the Green Tick button if they were sure about their prior choice of circles (high conﬁdence), and the Red Cross button if they were uncertain about it (low conﬁdence).
Choices were rewarded with a payoff scheme, such that the task amounted to a wagering procedure: 3 points were awarded for a high conﬁdence rating on a correct Type I response, −3 points for a high conﬁdence rating on an incorrect Type I response, and 1 point for a low conﬁdence wager, independent of correctness on the Type I response.

* PLAINEASY, SLIDEREASY, WAGEEASY. These are really easy versions of each type of trials. They are used as catch trials.

* PLAINHARD, SLIDERHARD, WAGEHARD. These are difficult versions of each type of trials. They are used also as catch trials too.



### Example

If you want to run an experiment with the following configuration of trials:

```
10 plain
10 wage
10 slider
1 plaineasy
1 plainhard
```

you will have to go to the settings component (click on it) and rewrite each line with the number of trials decided.

![settings](https://github.com/ababino/circles_metacog/blob/master/images/settings1.png)

```
wager = 10
slider = 10
plain = 10
wagereasy = 0
wagerhard = 0
slidereasy = 0
sliderhard = 0
plaineasy = 1
plainhard = 1
```

Levels

If you design a wage task, another parameter that is useful when planning the experiment is the total number of points that are mandatory to win a level and get to next. Given that participants will accumulate points according with their Type I and Type II responses.

In [Salles et al] the number of accumulated points was displayed as colored balls on the metacognitive report screen. When participants earned 9 points, they advanced to the next level and the counter was reset, the experiment continued until participants completed 10 levels.

This is important if you plan to run this experiment with children. In this case, you will need a game-like version of the experiment to avoid them to get tired or bored.

To change it, set the parameter listed in the seventh line of the code component.
For example if you want a child to collect 10 points to win a level, write:

```
points_to_pass_level = 10
```

If you want NO LEVEL STRUCTURE, set as many point as the number of wage trials times three (this is the maximum possible score). For our previous example this is 30:

```
points_to_pass_level = 30
```

Treatments

Likely, you will want to run the experiemnt in different treatment conditions.
Logging this changes into the data files makes easier the posterior analysis, that is why we add this variable inside the settings components.
In this way you will be able to give a name to each tratment with out showing it to the subjects.
Treatments could be 'Control' or 'Adults' or any string.
