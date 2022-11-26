from rest_framework.test import APIClient
import pytest
from students.models import Student, Course
from model_bakery import baker
from rest_framework.reverse import reverse


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    courses = course_factory(name='test')
    url = reverse('courses-detail', args=(courses.id,))
    response = client.get(url)
    data = response.json()
    course = Course.objects.filter(id=data['id'])

    assert response.status_code == 200
    assert data['id'] == course[0].id


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    courses =  course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, data={'id':courses[0].id})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses =  course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, data={'name':courses[0].name})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_course_create(client):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'course_new'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_course_update(client, course_factory):
    courses = course_factory(_quantity=1)
    url = reverse('courses-detail', args=(courses[0].id,))
    data = {'name': 'updated_course'}
    response = client.patch(url, data=data)

    assert response.status_code == 200
    assert response.data['name'] == 'updated_course'


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory(_quantity=1)
    url = reverse('courses-detail', args=(courses[0].id,))
    client.delete(url)
    response = client.get(url)
    data = response.json()

    assert response.status_code == 404
    assert courses[0].id not in data

