GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
        )

MATHPLAN_CHOICES = (
        ('', 'choose unit type'),
        ('li', 'lines'),
        ('ex','examples'),
        )

READINGPLAN_CHOICES = (
        ('', 'choose unit type'),
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

def gender_him_her(gender):
        return 'him' if gender == "M" else 'her'

def gender_he_she(gender):
        return 'he' if gender == "M" else 'she'



# def group_required(*group_names):
#     """Requires user membership in at least one of the groups passed in."""
#      from django.contrib.auth.decorators import user_passes_test
#      def in_groups(u):
#         if u.is_authenticated():
#             if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
#                 return True
#             return False
#     return user_passes_test(in_groups)

