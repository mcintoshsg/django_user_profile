from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase


from profiler.views import home
from accounts.models import UserProfile

user_data = {'username': 'stuartgordonmcintosh', 
             'first_name': 'stuart',
             'last_name': 'mcintosh',
             'email': 'stuart.mcintosh@test.com',
             'password1': 'XGEyPfoMRNYTo7A#yWLnKEht',
             'password2': 'XGEyPfoMRNYTo7A#yWLnKEht',
             'date_of_birth': '11/22/1963',
             'bio': 'this is my bio',
             'avatar': 'yosemite_bridge.jpg',
            }

login_data = {'username': 'stuartgordonmcintosh', 
              'password': 'XGEyPfoMRNYTo7A#yWLnKEht', } 

# test pages / views
class AccountsViewsTest(TestCase):
    ''' test of our views using post and get '''
    def setUp(self):
        self.c = Client()
        # self.user = User.objects.create(username=user_data['username'],
        #                                 first_name=user_data['first_name'],
        #                                 last_name=user_data['last_name'],
        #                                 password=user_data['password1'])
                                       
        # self.test_user1 = UserProfile.objects.create(user=self.user, 
        #                               date_of_birth='1963-11-22',
        #                               bio=user_data['bio'],
        #                               avatar='')
        # self.test_user1.save()



    def test_home_view(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_sign_up_view(self):
        response = self.c.get('/accounts/sign_up/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
        
    def test_sign_up_post_view(self):
        response = self.c.post('/accounts/sign_up/', user_data)
        self.assertRedirects(response,'/accounts/view_profile/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
        self.assertTrue(self.c.login(username='stuartgordonmcintosh', 
                                     password='XGEyPfoMRNYTo7A#yWLnKEht'))
    
        


# test modles
class UserProfileModelTest(TestCase):
    ''' test out the database'''
    def setUp(self):
        self.user = User.objects.create(username='some_user')
        self.test_user1 = UserProfile.objects.create(user=self.user, 
                                      date_of_birth='1963-11-22',
                                      bio='my life',
                                      avatar='')
        self.test_user1.save()

    def test_saving_and_retrieving_users(self):
        saved_users = UserProfile.objects.all()
        self.assertEqual(saved_users.count(), 1)
        self.assertEqual(saved_users[0].bio, 'my life')

#test forms

        