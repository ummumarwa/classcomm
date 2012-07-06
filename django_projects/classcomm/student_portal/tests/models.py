from django.utils import unittest
from django.contrib.auth.models import User
from classcomm.student_portal.models import *
from django.test import Client

# This line enables csrf checks in tests
# csrf_client = Client(enforce_csrf_checks=True)

class StudentModelTests(unittest.TestCase):
    """
    This class contains tests for the Model functionality of the student_portal app.
    
    """
    director_udata = {'username': 'Director',
                 'password': 'swordfish',
                 'email': 'alice@example.com'}
    instructor_udata = {'username': 'Instructor',
                 'password': 'test',
                 'email': 'beta@gamma.net'}
    mentor_udata = {'username': 'Mentor',
                 'password': 'tasty',
                 'email': 'sanderson@uiuc.com'}
    studentA_udata = {'username': 'StudentA',
                 'password': 'tasty',
                 'email': 'mjdavis2@uiuc.com'}
    studentB_udata = {'username': 'StudentB',
                 'password': 'tasty',
                 'email': 'sand@uiuc.com'}
    studentC_udata = {'username': 'StudentC',
                 'password': 'treats',
                 'email': 'doc@geekshack.net'}

    # def setUp(self):
        # self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        # settings.ACCOUNT_ACTIVATION_DAYS = 7

    # def tearDown(self):
        # settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation

    def test_create_users(self):
        """ Create our Meta test users based on Classcomm user roles. """
        self.director_u = User.objects.create_superuser(**self.director_udata)
        self.instructor_u = User.objects.create_user(**self.instructor_udata)
        self.mentor_u = User.objects.create_user(**self.mentor_udata)
        self.studentA_u = User.objects.create_user(**self.studentA_udata)
        self.studentB_u = User.objects.create_user(**self.studentB_udata)
        self.studentC_u = User.objects.create_user(**self.studentC_udata)

        # Verify the Director User  
        self.assertEqual(self.director_u.username, self.director_udata['username'])
        self.assertEqual(self.director_u.email, self.director_udata['email'])
        self.failUnless(self.director_u.check_password(self.director_udata['password']))

        # Verify Parts of each of the rest of the test Users
        self.assertEqual(self.instructor_u.username, self.instructor_udata['username'])
        self.assertEqual(self.instructor_u.email, self.instructor_udata['email'])
        self.failUnless(self.mentor_u.check_password(self.mentor_udata['password']))
        self.assertEqual(self.studentA_u.username, self.studentA_udata['username'])
        self.assertEqual(self.studentB_u.email, self.studentB_udata['email'])
        self.failUnless(self.studentC_u.check_password(self.studentC_udata['password']))
    # EndDef

    def test_departments(self):
        """ Create Department Models to test with. """
        self.NetMath_dept = Department.objects.create(name="NetMath")
        self.Biology_dept = Department.objects.create(name="Biology & Informatics")
        self.MachineLearning_dept = Department.objects.create(name="Machine Learning")

        # Basic Property checks
        self.assertEqual(self.NetMath_dept.name, "NetMath")
        self.assertEqual(self.Biology_dept.name, "Biology & Informatics")
        self.assertEqual(self.MachineLearning_dept.name, "Machine Learning")
    # EndDef

    def test_courses(self):
        """ Create Course Models to test with. """
        self.DifferentialEquations385 = Course.objects.create(department=self.NetMath_dept,
                                                name="385 Differential Equations",
                                                director=self.director_u,
                                                open_enrollments=True,
                                                enrollment_length=16,
                                                description="Course covers material on advanced differentials.")
        self.LinearAlgebra415 = Course.objects.create(department=self.NetMath_dept, name="415 Linear Algebra",
                                                director=self.director_u,
                                                open_enrollments=False,
                                                enrollment_length=16,
                                                description="Vectors, Matrices and Physical Space through n-dimensions.")
        self.SemiSupervisedLearning = Course.objects.create(department=self.MachineLearning_dept,
                                                name="Semi Supervised Learning",
                                                director=None,
                                                open_enrollments=False,
                                                enrollment_length=12,
                                                description="Computer SemiSupervised Learning.")

        # Check some properties
        self.assertEqual(self.DifferentialEquations385.name, "385 Differential Equations")
        self.failUnless(self.DifferentialEquations385.open_enrollments, "Differential Equations")
        self.assertEqual(self.LinearAlgebra415.director, self.director_u)
        self.assertEqual(self.SemiSupervisedLearning.description, "Computer SemiSupervised Learning.")
    # EndDef

    def test_assignments(self):
        """ Create Assignment Models to test with. """
        self.MGM001 = Assignment.objects.create(course=self.DifferentialEquations385,
                                                details="Complete Problems 01. 02. 03. 04. 05. 06. 08. 20.",
                                                points_possible=20, display_points_possible=True,
                                                provided_files=None, apply_due_date=True, weeks_after=False,
                                                allow_late=True, disable_submissions=True)
        self.MGM002 = Assignment.objects.create(course=self.DifferentialEquations385,
                                                details="Complete Problems 01. 02. 03. 04. 05. 06. 08. 10.",
                                                points_possible=20, display_points_possible=True,
                                                provided_files=None, apply_due_date=True, weeks_after=False,
                                                allow_late=False, disable_submissions=False)
    # EndDef

    #def test_assignments(self):
        """ Run some tests on our models """
        #self.assertEqual(self.lion.speak(), 'The lion says "roar"')
        #self.assertEqual(self.cat.speak(), 'The cat says "meow"')

    # def create_enrollments



# EndDef

