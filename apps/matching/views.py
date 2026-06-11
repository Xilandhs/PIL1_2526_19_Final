# apps/matching/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.matching.models import Competence
from apps.users.models import Users


def calculate_match_score(user_a, user_b, role):
    if role == 'mentor':
        common = Competence.objects.filter(
            user=user_b, type='competence',
            matiere__in=Competence.objects.filter(user=user_a, type='lacune').values('matiere')
        ).count()
        total = Competence.objects.filter(user=user_a, type='lacune').count()
        return round((common / total) * 100, 2) if total > 0 else 0
    else:
        common = Competence.objects.filter(
            user=user_a, type='competence',
            matiere__in=Competence.objects.filter(user=user_b, type='lacune').values('matiere')
        ).count()
        total = Competence.objects.filter(user=user_b, type='lacune').count()
        return round((common / total) * 100, 2) if total > 0 else 0


def get_common_subjects(user_a, user_b):
    return Competence.objects.filter(
        user=user_b, type='competence',
        matiere__in=Competence.objects.filter(user=user_a, type='lacune').values('matiere')
    ).select_related('matiere')[:5]


@login_required
def matching_view(request):
    user = request.user
    
    lacunes = Competence.objects.filter(user=user, type='lacune').values_list('matiere_id', flat=True)
    competences = Competence.objects.filter(user=user, type='competence').values_list('matiere_id', flat=True)
    
    mentors = []
    if lacunes:
        mentors = Users.objects.filter(
            competences__matiere_id__in=lacunes,
            competences__type='competence'
        ).exclude(id=user.id).distinct()
    
    mentees = []
    if competences:
        mentees = Users.objects.filter(
            competences__matiere_id__in=competences,
            competences__type='lacune'
        ).exclude(id=user.id).distinct()
    
    mentor_matches = []
    for mentor in mentors:
        score = calculate_match_score(user, mentor, 'mentor')
        common = get_common_subjects(user, mentor)
        mentor_matches.append({
            'user': mentor,
            'score': score,
            'common_subjects': common
        })
    
    mentee_matches = []
    for mentee in mentees:
        score = calculate_match_score(user, mentee, 'mentee')
        common = get_common_subjects(user, mentee)
        mentee_matches.append({
            'user': mentee,
            'score': score,
            'common_subjects': common
        })
    
    mentor_matches.sort(key=lambda x: x['score'], reverse=True)
    mentee_matches.sort(key=lambda x: x['score'], reverse=True)
    
    context = {
        'mentor_matches': mentor_matches[:10],
        'mentee_matches': mentee_matches[:10],
        'has_lacunes': len(lacunes) > 0,
        'has_competences': len(competences) > 0,
    }
    return render(request, 'pages/matching.html', context)