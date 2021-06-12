import logging
from django.contrib.contenttypes.models import ContentType
from apps.organizations.models import Branch, Organization
from apps.courses.models import Subject, Course
from apps.sessions.models import Session, Lecture, Module
from apps.users.models import Staff, User
from apps.enrollments.models import Enrollment
from apps.profiles.models import Profile, ProfileInteractionHistory
from apps.payments.models import Transaction
from apps.rooms.models import Room, VirtualRoom, VirtualRoomParticipant, VirtualRoomEvent
from apps.exams.models import Question, Choice, Answer, Attempt
from apps.attendances.models import Attendance
from apps.notifications.models import NotificationTask


logger = logging.getLogger(__name__)

def get_content_object(content_type, content_id):
    ct = ContentType.objects.get(model=content_type)
    ContentModel = ct.model_class()
    return ContentModel.objects.get(id=content_id)


def get_content_object_by_id(content_type_id, content_id):
    ct = ContentType.objects.get(id=content_type_id)
    ContentModel = ct.model_class()
    return ContentModel.objects.get(id=content_id)


def clone_branch(org_target_id, org_dest_id):
    """
    Returned the cloned organization
    """
    logger.debug("begin clone branch")
    mapping_old_new_branches = {}
    branches = Branch.objects.filter(organization__id=org_target_id)
    for branch in branches:
        old_id = branch.id
        branch.id=None
        branch.organization = get_content_object("organization", org_dest_id)
        branch.save()
        mapping_old_new_branches[old_id] = branch
    logger.debug(mapping_old_new_branches)
    return mapping_old_new_branches


def clone_staff(org_target_id, org_dest_id, branch_map):
    logger.debug("begin clone staff")
    staff_map = {}
    staffs = Staff.objects.filter(organization__id=org_target_id)
    for staff in staffs:
        old_id = staff.id
        old_branch_ids = staff.branches.all().values_list("id", flat=True)
        staff.id = None
        staff.organization = get_content_object("organization", org_dest_id)
        for branch_id in old_branch_ids:
            if not staff.id:
                staff.save()
                staff.branches.clear()
            staff.branches.add(branch_map[branch_id])
        staff.save()
        staff_map[old_id] = staff
    logger.debug(staff_map)
    return staff_map

def clone_profile(org_target_id, branch_map):
    logger.debug("begin clone profile")
    profile_map = {}
    profiles = Profile.objects.filter(branch__organization__id=org_target_id)
    for profile in profiles:
        old_id = profile.id
        profile.id = None
        profile.profile_code = ""
        profile.user = None
        profile.branch = branch_map[profile.branch.id]
        profile.organization = profile.branch.organization
        profile.latest_registration = None
        profile.latest_registration_state = ""
        profile.save()
        profile_map[old_id] = profile
    logger.debug(profile_map)
    return profile_map

def clone_subject(org_target_id, org_dest_id, staff_map):
    logger.debug("begin clone subject")
    subject_map = {}
    subjects = Subject.objects.filter(organization__id=org_target_id)
    for subject in subjects:
        old_id = subject.id
        subject.id = None
        subject.organization = get_content_object("organization", org_dest_id)
        if subject.creator:
            subject.creator = staff_map.get(subject.creator.id, None)
        subject.save()
        subject_map[old_id] = subject
    logger.debug(subject_map)
    return subject_map


def clone_course(org_target_id, branch_map, staff_map, subject_map):
    logger.debug("begin clone course")
    course_map = {}
    courses = Course.objects.filter(organization__id=org_target_id)
    for course in courses:
        old_id = course.id
        course.id = None
        course.branch = branch_map[course.branch.id]
        course.organization = course.branch.organization
        if course.subject:
            course.subject = subject_map.get(course.subject.id, None)
        if course.person_in_charge:
            course.person_in_charge = staff_map.get(course.person_in_charge.id, None)
        course.save()
        course_map[old_id] = course
    logger.debug(course_map)
    return course_map


def clone_room(org_target_id):
    logger.debug("begin clone room")
    room_map = {}
    rooms = Room.objects.filter(branch__organization__id=org_target_id)
    for room in rooms:
        old_id = room.id
        room.id = None
        room.save()
        room_map[old_id] = room
    return room_map


def clone_session(org_target_id, course_map, staff_map, room_map):
    session_map = {}
    sessions = Session.objects.filter(
        course__branch__organization__id=org_target_id)
    for session in sessions:
        old_id = session.id
        session.id = None
        if session.course:
            session.course = course_map.get(session.course.id)
        if session.teacher:
            session.teacher = staff_map.get(session.teacher.id)
        if session.room:
            session.room = room_map.get(session.room.id)
        session.save()
        session_map[old_id] = session
    return session_map


def clone_lecture(org_target_id, session_map):
    logger.debug("begin clone lecture")
    lecture_map = {}
    lectures = Lecture.objects.filter(session__course__branch__organization__id=org_target_id)
    for lecture in lectures:
        try:
            old_id = lecture.id
            lecture.id = None
            if lecture.session:
                lecture.session = session_map.get(lecture.session.id)
            lecture.save()
            lecture_map[old_id] = lecture
        except Exception as ex:
            print(str(ex))
    return lecture_map

def clone_module(org_target_id, lecture_map):
    logger.debug("begin clone module")
    module_map = {}
    modules = Module.objects.filter(lecture__session__course__branch__organization__id=org_target_id)
    for module in modules:
        old_id = module.id
        module.id = None
        if module.lecture:
            module.lecture = lecture_map.get(module.lecture.id)
        module.save()
        module_map[old_id] = module
    return module_map

def clone_enrollment(org_target_id, course_map, profile_map):
    logger.debug("begin clone enrollment")
    enrollments = Enrollment.objects.filter(
        course__branch__organization__id=org_target_id)
    for enrollment in enrollments:
        enrollment.id = None
        related_course = course_map.get(enrollment.course.id)
        related_profile = profile_map.get(enrollment.profile.id)
        if related_course and related_profile:
            enrollment.course = related_course
            enrollment.profile = related_profile
            enrollment.save()
        else:
            continue

def clone_transaction(org_target_id, branch_map, course_map, profile_map, staff_map):
    logger.debug("begin clone transaction")
    transactions = Transaction.objects.filter(organization__id=org_target_id)
    for transaction in transactions:
        transaction.id = None
        transaction.branch = branch_map[transaction.branch.id]
        transaction.organization = transaction.branch.organization
        transaction.course = course_map[transaction.course.id]
        transaction.profile = profile_map[transaction.profile.id]
        if transaction.staff:
            transaction.staff = staff_map[transaction.staff.id]
        transaction.save()


def clone_profile_interaction(org_target_id, profile_map, course_map):
    logger.debug("clone profile interaction histories")
    interactions = ProfileInteractionHistory.objects.filter(
        profile__branch__organization__id=org_target_id)
    for interaction in interactions:
        interaction.id = None
        interaction.profile = profile_map.get(interaction.profile.id)
        if interaction.course:
            interaction.course = course_map[interaction.course.id]
        interaction.save()


def clone_exams(org_target_id, lecture_map):
    question_map = {}
    choice_map = {}
    questions = Question.objects.filter(
        lecture__session__course__branch__organization__id=org_target_id)
    for question in questions:
        old_id = question.id
        question.id = None
        if question.lecture:
            question.lecture = lecture_map.get(question.lecture.id)
        question.save()
        question_map[old_id] = question
        choices = Choice.objects.filter(question__id=old_id)
        for choice in choices:
            old_choice_id = choice.id
            choice.id = None
            choice.question = question
            choice.save()
            choice_map[old_choice_id] = choice
    return question_map, choice_map


def clone_attempt(org_target_id, profile_map, lecture_map):
    ret_map = {}
    attempts = Attempt.objects.filter(
        profile__branch__organization__id=org_target_id)
    for attempt in attempts:
        old_id = attempt.id
        attempt.id = None
        attempt.profile = profile_map.get(attempt.profile.id)
        if attempt.lecture:
            attempt.lecture = lecture_map.get(attempt.lecture.id)
        attempt.save()
        ret_map[old_id] = attempt
    return ret_map

def clone_answer(org_target_id, question_map, choice_map, attempt_map):
    answers = Answer.objects.filter(
        attempt__profile__branch__organization__id=org_target_id)
    for ans in answers:
        ans.id = None
        ans.attempt = attempt_map.get(ans.attempt.id)
        ans.question = question_map.get(ans.question.id)
        choices = list(ans.choices)
        new_choices = []
        for choice in choices:
            new_choice = choice_map.get(choice)
            if new_choice:
                new_choices.append(new_choice.id)
        ans.choices = new_choices
        ans.save()

def clone_attendance(org_target_id, profile_map, session_map):
    attendances = Attendance.objects.filter(
        profile__branch__organization__id=org_target_id)
    for attendance in attendances:
        attendance.id = None
        attendance.profile = profile_map.get(attendance.profile.id)
        attendance.session = session_map.get(attendance.session.id)
        attendance.save()


def clone_vroom(org_target_id, session_map, staff_map):
    ret_map = {}
    vrooms = VirtualRoom.objects.filter(
        session__course__branch__organization__id=org_target_id)
    for vroom in vrooms:
        old_id = vroom.id
        vroom.id = None
        if vroom.session:
            vroom.session = session_map.get(vroom.session.id)
        if vroom.creator:
            vroom.creator = staff_map.get(vroom.creator.id)
        if vroom.moderator:
            vroom.moderator = staff_map.get(vroom.moderator.id)
        vroom.config = None
        vroom.save()
        ret_map[old_id] = vroom
    return ret_map


def clone_noti_task(org_target_id, org_dest_id, branch_map, course_map, staff_map):
    noti_tasks = NotificationTask.objects.filter(
        branch__organization__id=org_target_id
    )
    ret_map = {}
    for noti_task in noti_tasks:
        old_id = noti_task.id
        noti_task.id = None
        if noti_task.content_type:
            content_object = get_content_object_by_id(
                noti_task.content_type, noti_task.content_id)
            if isinstance(content_object, Course):
                noti_task.content_id = course_map.get(content_object.id).id
            else:
                noti_task.content_id = None
        if noti_task.sender_type:
            sender_object = get_content_object_by_id(
                noti_task.sender_type, noti_task.sender_id)
            if isinstance(sender_object, Staff):
                noti_task.sender_id = staff_map.get(sender_object.id).id
            elif isinstance(sender_object, User):
                noti_task.sender_id = None
                ### TO BE impl here
                # noti_task.sender_id = user_map.get(sender_object.id).id
        noti_task.organization = get_content_object(
            "organization", org_dest_id)
        noti_task.branch = branch_map.get(noti_task.branch.id)
        noti_task.save()
        ret_map[old_id] = noti_task
    return ret_map

def start_clone(org_target_id, org_dest_id):
    logger.debug("--- start clone")
    branch_map = clone_branch(org_target_id, org_dest_id)
    staff_map = clone_staff(org_target_id, org_dest_id, branch_map)
    subject_map = clone_subject(org_target_id, org_dest_id, staff_map)
    course_map = clone_course(org_target_id, branch_map, staff_map, subject_map)
    profile_map = clone_profile(org_target_id, branch_map)
    clone_profile_interaction(org_target_id, profile_map, course_map)
    clone_enrollment(org_target_id, course_map, profile_map)
    clone_transaction(org_target_id, branch_map, course_map, profile_map, staff_map)
    room_map = clone_room(org_target_id)
    session_map = clone_session(org_target_id, course_map, staff_map, room_map)
    lecture_map = clone_lecture(org_target_id, session_map)
    module_map = clone_module(org_target_id, lecture_map)
    question_map, choice_map = clone_exams(org_target_id, lecture_map)
    attempt_map = clone_attempt(org_target_id, profile_map, lecture_map)
    clone_answer(org_target_id, question_map, choice_map, attempt_map)
    clone_attendance(org_target_id, profile_map, session_map)
    vroom_map = clone_vroom(org_target_id, session_map, staff_map)
    noti_task_map = clone_noti_task(org_target_id, org_dest_id, branch_map, course_map, staff_map)