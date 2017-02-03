Title: You need a doorbell
Date: 2017-02-03
Category: programming
Tags: life, programming, python, twilio, flask
Slug: you-need-a-doorbell
Authors: Micah Smith

Sometimes a dumb technical approach can be a solution to a real world problem.

I live in a graduate residence that doesn't have a buzzer system. To be granted access, my
guests have to text/call me directly and I have to walk downstairs to let them in. Though
this may not seem like a big deal, if I'm having more than just a couple people over, it can
be a bit much to continuously be checking my phone and interrupting conversations to sprint
through hallways to the door.

I know it's not just me. Two of my friends had an apartment near me, when I lived in New
York, on Mott Street. Their apartment building, which was built in 1900, had no buzzer
system, even though it probably housed 50 people or more (and cost more than your parents'
mortgage payment per month for about 12 square feet of space). When friends were coming
over, the new arrivals would text to announce that they were outside, and my friends would
*drop the front door key in a sock out the window* onto the busy street. Somehow no one was
ever injured, and it sure was a lot of fun.

The approach I take here is to make the arrival process more seamless and transfer
burden of opening the door off the party hosts and onto the guests. Go ahead and design a
robot that turns a doorknob on command at your own peril.

## Introducing *you-need-a-doorbell*

[*you-need-a-doorbell*](https://github.com/micahjsmith/you-need-a-doorbell) is a simple app
that uses text messages and audio alerts to manage your guests' arrival to the party. When
they arrive, guests text a phone number that you have registered through Twilio. (Not your
own cell!) Their contact information is validated against permission lists, and if the guest
is authorized to enter the party, an announced is made from your computer speakers.
> DING DONG! Guest Flo Rida has arrived to the party.

Since everybody in the party can hear this announcement, it gives you, the host, latitude to
spin on your heels and point to some unsuspecting soul: "Go let Flo Rida in!"

The host can even have the app randomly assign responsibility to open the door from the
list of guests who have already arrived. This further removes responsibility from your plate
as now, not only are you not running down to open the door, but you're not even pointing
a finger at anyone! (And everyone knows computers are blameless.)

[Check out *you-need-a-doorbell* on GitHub.](https://github.com/micahjsmith/you-need-a-doorbell)

## Making the app

A simple Flask web server runs on my macOS desktop. Then, when a guest sends a text to the
party-specific phone number, the text message number and body are packaged into a POST
request to a URL on my server. After validation of the phone number, a text-to-speech
utility like `say` is used to play a message out of the speakers. The original version I
whipped up for a small kickback at my place was only 49 lines of code.

I added new features after my own alpha test and packaged things more nicely so that options
could be specified in a config file. I really enjoyed making this, as I learned a bit about
Flask and admired the simplicity of the Twilio API.

Going forward, I would re-design this so that the app was hosted in the cloud and party
hosts could access everything through a web interface. The server could run on EC2 or some
other service, listening for requests from Twilio. Simultaneously, the party host would log
in to the server. A connection would be kept open using a web socket. There, they could
manage permissions for potential guests, view those who had arrived (or those that were
still expected), and listen for arrival messages. One could even import attendance info from
a Facebook event. Perhaps, as I continue to learn more about web development, I'll create
this interface. For now, I'm happy with what I have, and I hope you may be too.

Since I added new features after my alpha test and didn't do very thorough testing, you may
find some bugs. Please let me know if that's the case.

I found that the text message interface for guests worked really well. It's interesting how
everyone and their mother releases iOS/Android apps to facilitate just simple messaging with
their organization and access to static resources like maps or schedules. I'm not sure that
this interface is any better than a text message hotline and a website. As "bots" are
becoming the rage for many simple tasks, maybe we'll see the lowly SMS make more of a
resurgence.
