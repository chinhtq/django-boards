# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve

from board.forms import NewTopicForm
from board.models import Board, Topic, Post
from board.views import home, board_topic, new_topic


# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Python', description='This is a board about Python')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topic', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Java', description='This is a board about Java')


    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topic',kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topic',kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/board/1/')
        self.assertEquals(view.func, board_topic)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topic_url = reverse('board_topic', kwargs={'pk':1})
        response = self.client.get(board_topic_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Java', description='This is a board about Java')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/board/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(new_topic_url)
        board_topic_url = reverse('board_topic', kwargs={'pk':1})
        self.assertContains(response,'href="{0}'.format(board_topic_url))

    def test_board_topics_view_contains_navigation_links(self):
        board_topic_url = reverse('board_topic', kwargs={'pk':1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk':1})

        response = self.client.get(board_topic_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response,'href="{0}"'.format(new_topic_url))

    def test_csrf(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response,'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject':'Test title',
            'message': 'Lorem ipsum dolor sit amet',
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': '',
            'message': '',
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)