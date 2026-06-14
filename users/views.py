@login_required
def settings_view(request):
    return render(request, 'pages/settings.html', {'user': request.user})

@login_required
def change_password_view(request):
    from django.contrib.auth import update_session_auth_hash
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not request.user.check_password(old_password):
            messages.error(request, 'Mot de passe actuel incorrect')
        elif new_password != confirm_password:
            messages.error(request, 'Les mots de passe ne correspondent pas')
        elif len(new_password) < 8:
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Mot de passe modifié avec succès')
        return redirect('settings')
    return redirect('settings')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            request.user.delete()
            messages.success(request, 'Votre compte a été supprimé')
            return redirect('home')
        else:
            messages.error(request, 'Mot de passe incorrect')
            return redirect('settings')
    return redirect('settings')