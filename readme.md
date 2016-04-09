#QNotifications
Many web applications have pretty in-app notifications nowadays. Wouldn't it be nice if something like that would also exist for PyQt applications and is very easy to integrate? That's the aim of this project: to provide a system that can display several types of notifications (info, errors, warnings, etc.) and which can easily be plugged into existing PyQt projects. 

In the design of this system, we try to adhere to the Gnome UI guidlines for in-app notifications (https://developer.gnome.org/hig/stable/in-app-notifications.html.en) as much as possible. A current exception, is that this system allows multiple notifications to be displayed simultaneously (they will be stacked on top of each other), while best practice is to display multiple notifications sequentially but only one a the time. There currently is not yet an option to do the latter.

## Example
Elaborate examples with code soon to be given here.
For now, to see it in action just run
    
    python example.py


## Styling
The Notifications' styles can be altered through style-sheets. More instructions soon to follow.

## API
Documentation / API soon to follow. 