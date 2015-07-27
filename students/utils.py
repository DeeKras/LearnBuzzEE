GROUPS_LIST = (
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D')
        )

GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
        )

MATHPLAN_CHOICES = (
        ('li', 'lines'),
        ('ex','examples'),
        )

READINGPLAN_CHOICES = (
        ('li', 'lines'),
        ('pg','pages'),
        ('ch', 'chapters'),
        ('bk','books'),
        )


def get_display(choice_list, code):
        return next(extended for shortened, extended in choice_list if shortened==code)


def strip_html(html):
        import re, cgi
        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        no_tags = tag_re.sub('', html)
        ready_for_web = cgi.escape(no_tags)
        return ready_for_web