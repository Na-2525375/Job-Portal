from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages

from myApp.models import *


def signupPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        displayname= request.POST.get('display_name')
        mail= request.POST.get('email')
        pass_word= request.POST.get('password')
        usertype= request.POST.get('user_type')
        user = Custom_User.objects.create_user(username=user_name,password=pass_word)
        user.display_name=displayname
        user.email=mail
        user.user_type=usertype
        user.save()

        if user.user_type == 'recruiter':
            user=RecruiterProfile.objects.create(user=user)
            user.save()
        else:
            user=JobSeekerProfile.objects.create(user=user)
            user.save()

        return redirect("signinPage")

    return render(request,'signup.html')

def logoutPage(request):

    logout(request)

    return redirect('signinPage')

def signinPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=user_name, password=password)

        print(user)

        if user:
            login(request,user)
            return redirect("dashboardPage")


    return render(request,'login.html')

@login_required
def dashboardPage(request):

    return render(request,"dashboard.html")

@login_required
def viewjobPage(request):

    job=job_model.objects.all()

    context={
        'job':job
    }
    return render(request,"viewjob.html",context)

def add_job_Page(request):

    user = request.user

    if request.method == 'POST':

        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')

        job=job_model(
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            job_creator=user,
        )
        job.save()

        return redirect("viewjobPage")
    

    return render(request,'Recruiter/Addjob.html')

def deletePage(request,myid):

    job=job_model.objects.filter(id=myid)
    job.delete()

    return redirect("viewjobPage")

def editPage(request,myid):

    job=job_model.objects.filter(id=myid)

    return render(request,'Recruiter/editJob.html',{'job':job})

def updatePage(request):

    user = request.user
    if request.method == 'POST':

        job_id=request.POST.get('jobid')
        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')
        job=job_model(
            id=job_id,
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            job_creator=user,
        )
        job.save()
        return redirect("viewjobPage")


def applyPage(request,myid):

    job=get_object_or_404(job_model,id=myid)

    if request.method == 'POST':
        skills=request.POST.get('skills')
        myresume=request.FILES.get('resume')

        print(skills,myresume)

        if skills and myresume:
            job_seeker=request.user
        
            application=jobApplyModel.objects.create(
            job=job,
            applicant=job_seeker,
            skills=skills,
            apply_resume=myresume,
            )
            print(application)
            application.save()
        else:
            messages.error(request,'Error in application form, Please check it!')

        messages.success(request,'Apply Successfully')

        return redirect("ProfilePage")
    
    context={
        'job':job
    }

    return render(request,'JobSeeker/applyjob.html',context)

def ProfilePage(request):

    return render(request,'profile.html')

def EditProfilePage(request):

    user=request.user

    if request.method == 'POST':

        user_id= request.POST.get('user_id')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        display_name= request.POST.get('display_name')
        email= request.POST.get('email')
        image= request.FILES.get('profile_picture')
        entered_password= request.POST.get('password')
        myResume= request.FILES.get('myResume')
        mySkills= request.POST.get('mySkills')

        if not check_password(entered_password,user.password):
            messages.error(request,'Profile not updated, Wrong Password')
            return redirect("EditProfilePage")
        
        user.id=user_id
        user.first_name=first_name
        user.last_name=last_name
        user.display_name=display_name

        if user.user_type=='jobseeker':
            job_seeker_profile=user.jobseekerprofile
            job_seeker_profile.skills=mySkills
            job_seeker_profile.resume=myResume
            job_seeker_profile.save()

        if image:
            user.profile_picture=image

        user.save()
        messages.success(request,'Profile Updated Successfully')
        return redirect("ProfilePage")
        
    return render(request,'Editprofile.html')


def changePasswordPage(request):

    user=request.user

    if request.method == 'POST':

        old_password=request.POST.get('current_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')


        if not check_password(old_password,user.password):
            messages.error(request,'Wrong Current Password')
            return redirect("changePasswordPage")
        if new_password!=confirm_password:
            messages.error(request,'New password and Confirm Password Not Matched')
            return redirect("changePasswordPage")
        else:
            user.set_password(confirm_password)
            user.save()
            return redirect("signinPage")

    return render(request,'changepassword.html')


def createdJobByRecruiter(request):

    user=request.user

    creator=job_model.objects.filter(job_creator=user)

    context={
        'creator':creator
    }


    return render(request,'createdJob.html',context)


def applied_job_by_jobseeker(request):

    jobseekeruser=request.user

    applied_job=jobApplyModel.objects.filter(applicant=jobseekeruser)

    context={
        'applied':applied_job
    }
    return render(request,'JobSeeker/appliedjob.html',context)

def applicants_view_page(request,myid):

    myjob=get_object_or_404(job_model,id=myid)
    job=jobApplyModel.objects.filter(job=myjob)

    context={
        'myjob':myjob,
        'job':job,
    }


    return render(request,'Recruiter/applicants_view_page.html',context)
    






    