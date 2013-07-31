# TODO.md

In no particular order:

+ Don't sleep after there are no more keywords.
+ Add statistics/tracking 
  - how long the script spends working, 
  - how much time it spends delaying to avoid getting caught by Google
+ ability/option to create a log.txt or something (in case I need to troubleshoot)
+ detect if Autoscraper has triggered Google's 'Sorry' message;
  - after which it should trigger a larger delay,
  - change useragent,
  - and then resume queries
    + and if it is otherwise resuming queries (i.e. running the program twice), 
      it should also check the current results.csv, to make sure it's not adding duplicate rows.
    + consider adding support for reading in old .csv files,
      - and tracking whether or not rankings are improving or not
+ Make this is less-detectable by Google.
+ Check and make sure that the results produced by this file are the same as 'organic' searches,
  - and perhaps the ability to assume the user's useragent and cookies, in order to
    double-check and ensure that results returned by this program are useful
+ Support for more complex domains/pages
+ Support for functions which allow on-demand loading of new keyword, domain, and useragent files. Maybe.
