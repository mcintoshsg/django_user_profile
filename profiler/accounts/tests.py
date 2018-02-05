from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase


from profiler.views import home
from accounts.models import UserProfile

user_data1 = {'username': 'stuartgordonmcintosh', 
             'first_name': 'stuart',
             'last_name': 'mcintosh',
             'email': 'stuart.mcintosh@test.com',
             'password1': 'XGEyPfoMRNYTo7A#yWLnKEht',
             'password2': 'XGEyPfoMRNYTo7A#yWLnKEht',
             'date_of_birth': '1963-11-22',
             'bio': 'this is my bio',
             'avatar': '',
            }

user_data2 = {'username': 'stuartmcintosh', 
             'first_name': 'stuart',
             'last_name': 'mcintosh',
             'email': 's.mcintosh@test.com',
             'password1': 'XGEyPfoMRNYTo7A#yWLnKEht',
             'password2': 'XGEyPfoMRNYTo7A#yWLnKEht',
             'date_of_birth': '11/22/1963',
             'bio': 'this is my awful bio',
             'avatar': '',
            }

# test modles
class UserProfileModelTest(TestCase):
    ''' test out the database'''
    def setUp(self):
        self.user1 = User.objects.create(username=user_data1['username'],
                                        first_name=user_data1['first_name'],
                                        last_name=user_data1['last_name'],
                                        password=user_data1['password1'])
        self.test_user1 = UserProfile.objects.create(user=self.user1, 
                                      date_of_birth=user_data1['date_of_birth'],
                                      bio=user_data1['bio'],
                                      avatar='')
        self.test_user1.save()

    def test_saving_and_retrieving_users(self):
        saved_users = UserProfile.objects.all()
        self.assertEqual(saved_users.count(), 1)
        self.assertEqual(saved_users[0].bio, 'this is my bio')

# test pages / views
class AccountsViewsTest(TestCase):
    ''' test of our views using post and get '''
    def setUp(self):
        self.c = Client()
        self.user1 = User.objects.create(username=user_data1['username'],
                                        first_name=user_data1['first_name'],
                                        last_name=user_data1['last_name'],
                                        password=user_data1['password1'])
        self.user1.is_active = True
        self.user1.save()                                
                                       
        self.test_user1 = UserProfile.objects.create(user=self.user1, 
                                      date_of_birth='1963-11-22',
                                      bio=user_data1['bio'],
                                      avatar='')
                                      
        self.test_user1.is_active = True                              
        self.test_user1.save()
        

    def test_home_view(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_sign_up_view(self):
        response = self.c.get('/accounts/sign_up/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
        
    def test_sign_up_post_view(self):
        response = self.c.post('/accounts/sign_up/', user_data2)
        self.assertRedirects(response,'/accounts/view_profile/')
        self.assertTrue(self.c.login(username=user_data2['username'], 
                                     password=user_data2['password1']))

    def test_sign_in_post_view(self):
        response = self.c.get('/accounts/sign_in/')
        self.assertTemplateUsed(response, 'accounts/sign_in.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign In' in str(response.content))
        response = self.c.post('/accounts/sign_in/',
                              {'username': user_data1['username'], 
                               'password': user_data1['password1']})
        self.assertEqual(response.status_code, 302)                       
        self.assertRedirects(response,'/accounts/view_profile/')
        
        
