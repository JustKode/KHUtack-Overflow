from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, user_id, name, student_id,
                    birth, email, phone, password=None, **extra_fields):
        """
        아이디, 비밀번호, 이름, 학번으로 계정 생성
        """
        if not user_id:
            raise ValueError('Users must have a user id.')

        user = self.model(
            user_id=user_id,
            name=name,
            student_id=student_id,
            birth=birth,
            phone=phone,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, student_id,
                         birth, email, phone, password=None, **extra_fields):
        """
        아이디, 비밀번호, 이름, 학번으로 슈퍼 계정 생성
        """

        user = self.create_user(
            user_id=user_id,
            password=password,
            name=name,
            student_id=student_id,
            birth=birth,
            phone=phone,
            email=email,
            **extra_fields
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.CharField(
        verbose_name='아이디',
        max_length=20,
        unique=True
    )
    name = models.CharField(
        verbose_name='이름',
        max_length=20
    )
    birth = models.DateField(
        verbose_name='생일',
    )
    is_active = models.BooleanField(
        verbose_name='계정 활성화',
        default=True
    )  # 활성화 여부
    is_admin = models.BooleanField(
        verbose_name='어드민 여부',
        default=False
    )  # 어드민 여부
    student_id = models.CharField(
        verbose_name='학번',
        max_length=10
    )  # 학번
    email = models.EmailField(
        verbose_name='이메일',
        max_length=255,
        unique=True
    )
    phone = models.CharField(
        verbose_name='전화번호',
        max_length=20
    )
    github = models.CharField(
        verbose_name='Github 닉네임',
        max_length=20,
        default='null'
    )
    homepage = models.URLField(
        verbose_name='개인 블로그 주소',
        max_length=200,
        default='http://ce.khu.ac.kr/'
    )

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'student_id', 'birth', 'email', 'phone']

    def __str__(self):
        return self.admission_year + ' ' + self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
