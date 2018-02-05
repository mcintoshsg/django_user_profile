from django.contrib.auth.models import User
from django.contrib.auth import get_user, get_user_model
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase


from profiler.views import home
from accounts.models import UserProfile

user_data1 = {'username': 'stuartmcintosh', 
             'first_name': 'stuart',
             'last_name': 'mcintosh',
             'email': 's.mcintosh@test.com',
             'password': 'XGEyPfoMRNYTo7A#yWLnKEht',
            }

sign_up_data1 = {'username': 'stuartgordonmcintosh', 
                 'first_name': 'stuart',
                 'last_name': 'gordon',
                 'email': 's.g.mcintosh@test.com',
                 'password1': 'XGEyPfoMRNYTo7A#yWLnKEht',
                 'password2': 'XGEyPfoMRNYTo7A#yWLnKEht',
                 'date_of_birth': '1963-11-22',
                 'bio': 'this is my life',
                 'avatar': '',
            }

# test pages / views
class AccountsViewsTest(TestCase):
    ''' test of our views using post and get '''
    
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(**user_data1)
        
        self.userprofile1 = UserProfile.objects.create(
            user=self.user1,
            date_of_birth='1963-11-22',
            bio='this is my life',
            avatar=''
        )    

    def login(self):
        self.client.login(username='stuartmcintosh', 
                     password='XGEyPfoMRNYTo7A#yWLnKEht')
        user = get_user(self.client)
        if user.is_authenticated():             
            return True             
        else:
            return False


    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_sign_up_view(self):
        response = self.client.get('/accounts/sign_up/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
        
    def test_sign_up_post_view(self):
        response = self.client.post('/accounts/sign_up/', sign_up_data1)
        self.assertRedirects(response,'/accounts/view_profile/')
        self.assertTrue(self.client.login(
                        username='stuartgordonmcintosh', 
                        password='XGEyPfoMRNYTo7A#yWLnKEht')
                        )

    def test_sign_in_post_view(self):
        response = self.client.get('/accounts/sign_in/')
        self.assertTemplateUsed(response, 'accounts/sign_in.html')
        self.assertEqual(response.status_code, 200)
       
        response = self.client.post('/accounts/sign_in/',
                                   {'username': 'stuartmcintosh', 
                                    'password': 'XGEyPfoMRNYTo7A#yWLnKEht'}
                                    )
        self.assertRedirects(response, '/accounts/view_profile/', 
                             fetch_redirect_response=False
                             )
    
    def test_sign_out_post_view(self):   
        if self.login():
            self.client.post('/accounts/sign_out/')
            user = get_user(self.client)
            self.assertFalse(user.is_authenticated(), False)
        else:
            print("user not logged in!!!")

    def test_view_profile_view(self):
        if self.login():
            response = self.client.get('/accounts/view_profile/')
            self.assertTrue('View Profile' in str(response.content))
        else:
            print("user not logged in!!!")
    
    def test_edit_profile_view(self):
        pass


    def test_change_password_view(self):
        pass

    

# test modles
class UserProfileModelTest(TestCase):
    ''' test out the database'''
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(
            username = 'stuartmcintosh',
            first_name='stuart',
            last_name='mcintosh',
            email='stuart.mcintosh@test.com',
            password='XGEyPfoMRNYTo7A#yWLnKEht'
        )
        
        self.userprofile1 = UserProfile.objects.create(
            user=self.user1,
            date_of_birth='1963-11-22',
            bio='this is my life',
            avatar=''
        )    
        
    def test_saving_and_retrieving_users(self):
        saved_users = UserProfile.objects.all()
        self.assertEqual(saved_users.count(), 1)
        self.assertEqual(saved_users[0].bio, 'this is my life')