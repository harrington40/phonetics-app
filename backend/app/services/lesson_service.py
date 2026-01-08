from datetime import datetime
from app.db.connection import db
from app.models.schemas import Lesson, VisemeCue, UserProgress
import uuid

class LessonService:
    """Service for lesson management"""

    SAMPLE_LESSONS = [
        {
            "id": "lesson_p",
            "phoneme": "/p/",
            "prompt": "Let's pop like a puppy! Say: p p p",
            "audio_url": "https://example.com/audio/p.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "round", "start_ms": 120, "end_ms": 220},
                {"viseme": "open", "start_ms": 220, "end_ms": 330},
                {"viseme": "rest", "start_ms": 330, "end_ms": 600},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_m",
            "phoneme": "/m/",
            "prompt": "Mmm like yummy muffin! Say: m m m",
            "audio_url": "https://example.com/audio/m.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "smile", "start_ms": 120, "end_ms": 260},
                {"viseme": "rest", "start_ms": 260, "end_ms": 600},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_s",
            "phoneme": "/s/",
            "prompt": "Sssss like a friendly snake! Say: s s s",
            "audio_url": "https://example.com/audio/s.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_t",
            "phoneme": "/t/",
            "prompt": "Ttt like a tiny tiger! Say: t t t",
            "audio_url": "https://example.com/audio/t.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "rest", "start_ms": 250, "end_ms": 400},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_n",
            "phoneme": "/n/",
            "prompt": "Nnn like a noisy nose! Say: n n n",
            "audio_url": "https://example.com/audio/n.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "smile", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_b",
            "phoneme": "/b/",
            "prompt": "Bbb like a big bear! Say: b b b",
            "audio_url": "https://example.com/audio/b.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "round", "start_ms": 120, "end_ms": 220},
                {"viseme": "open", "start_ms": 220, "end_ms": 330},
                {"viseme": "rest", "start_ms": 330, "end_ms": 500},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_d",
            "phoneme": "/d/",
            "prompt": "Ddd like a dancing dog! Say: d d d",
            "audio_url": "https://example.com/audio/d.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "rest", "start_ms": 250, "end_ms": 400},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_k",
            "phoneme": "/k/",
            "prompt": "Kkk like a crazy cat! Say: k k k",
            "audio_url": "https://example.com/audio/k.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "open", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_g",
            "phoneme": "/g/",
            "prompt": "Ggg like a goofy gorilla! Say: g g g",
            "audio_url": "https://example.com/audio/g.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "open", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_f",
            "phoneme": "/f/",
            "prompt": "Fff like a funny fox! Say: f f f",
            "audio_url": "https://example.com/audio/f.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 300},
                {"viseme": "rest", "start_ms": 300, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_a",
            "phoneme": "/a/",
            "prompt": "Aaa like an apple! Say: a a a",
            "audio_url": "https://example.com/audio/a.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_e",
            "phoneme": "/e/",
            "prompt": "Eee like an elephant! Say: e e e",
            "audio_url": "https://example.com/audio/e.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_i",
            "phoneme": "/i/",
            "prompt": "Iii like an igloo! Say: i i i",
            "audio_url": "https://example.com/audio/i.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_o",
            "phoneme": "/o/",
            "prompt": "Ooo like an octopus! Say: o o o",
            "audio_url": "https://example.com/audio/o.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_u",
            "phoneme": "/u/",
            "prompt": "Uuu like an umbrella! Say: u u u",
            "audio_url": "https://example.com/audio/u.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_sh",
            "phoneme": "/sh/",
            "prompt": "Shhh like a quiet library! Say: sh sh sh",
            "audio_url": "https://example.com/audio/sh.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_ch",
            "phoneme": "/ch/",
            "prompt": "Chh like a choo-choo train! Say: ch ch ch",
            "audio_url": "https://example.com/audio/ch.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 300},
                {"viseme": "rest", "start_ms": 300, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_th",
            "phoneme": "/th/",
            "prompt": "Thhh like thunder! Say: th th th",
            "audio_url": "https://example.com/audio/th.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_cat",
            "phoneme": "cat",
            "prompt": "Can you say CAT? Let's try it together!",
            "audio_url": "https://example.com/audio/cat.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "open", "start_ms": 250, "end_ms": 400},
                {"viseme": "open", "start_ms": 400, "end_ms": 550},
                {"viseme": "rest", "start_ms": 550, "end_ms": 700},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_dog",
            "phoneme": "dog",
            "prompt": "Can you say DOG? Woof woof!",
            "audio_url": "https://example.com/audio/dog.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "round", "start_ms": 250, "end_ms": 400},
                {"viseme": "open", "start_ms": 400, "end_ms": 550},
                {"viseme": "rest", "start_ms": 550, "end_ms": 700},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_v",
            "phoneme": "/v/",
            "prompt": "Vvv like a victorious vulture! Say: v v v",
            "audio_url": "https://example.com/audio/v.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 300},
                {"viseme": "rest", "start_ms": 300, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_h",
            "phoneme": "/h/",
            "prompt": "Hhh like a happy horse! Say: h h h",
            "audio_url": "https://example.com/audio/h.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "open", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_l",
            "phoneme": "/l/",
            "prompt": "Lll like a lazy lion! Say: l l l",
            "audio_url": "https://example.com/audio/l.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "smile", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_r",
            "phoneme": "/r/",
            "prompt": "Rrr like a roaring rabbit! Say: r r r",
            "audio_url": "https://example.com/audio/r.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 300},
                {"viseme": "rest", "start_ms": 300, "end_ms": 450},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_w",
            "phoneme": "/w/",
            "prompt": "Www like a wiggly worm! Say: w w w",
            "audio_url": "https://example.com/audio/w.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "round", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_y",
            "phoneme": "/y/",
            "prompt": "Yyy like a yodeling yak! Say: y y y",
            "audio_url": "https://example.com/audio/y.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                {"viseme": "smile", "start_ms": 120, "end_ms": 280},
                {"viseme": "rest", "start_ms": 280, "end_ms": 450},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # Missing Consonants
        {
            "id": "lesson_j",
            "phoneme": "/j/",
            "prompt": "Jjj like a jumping jaguar! Say: j j j",
            "audio_url": "https://example.com/audio/j.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "rest", "start_ms": 250, "end_ms": 400},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_z",
            "phoneme": "/z/",
            "prompt": "Zzz like a buzzing bee! Say: z z z",
            "audio_url": "https://example.com/audio/z.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_x",
            "phoneme": "/ks/",
            "prompt": "X-x-x like a fox in a box! Say: x x x",
            "audio_url": "https://example.com/audio/x.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_qu",
            "phoneme": "/kw/",
            "prompt": "Qu-qu like a quacking duck! Say: qu qu qu",
            "audio_url": "https://example.com/audio/qu.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "round", "start_ms": 200, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # Essential Digraphs
        {
            "id": "lesson_wh",
            "phoneme": "/hw/",
            "prompt": "Wh-wh like the wind whistles! Say: wh wh wh",
            "audio_url": "https://example.com/audio/wh.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 250},
                {"viseme": "open", "start_ms": 250, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_ng",
            "phoneme": "/ŋ/",
            "prompt": "Ng-ng like a ringing bell! Say: ng ng ng",
            "audio_url": "https://example.com/audio/ng.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_ck",
            "phoneme": "/k/",
            "prompt": "Ck-ck like a clock tick-tock! Say: ck ck ck",
            "audio_url": "https://example.com/audio/ck.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "rest", "start_ms": 250, "end_ms": 400},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_th_voiced",
            "phoneme": "/ð/",
            "prompt": "Th-th like THIS and THAT! Say: th th th",
            "audio_url": "https://example.com/audio/th_voiced.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 350},
                {"viseme": "rest", "start_ms": 350, "end_ms": 500},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # Long Vowels with Silent E
        {
            "id": "lesson_cake",
            "phoneme": "cake",
            "prompt": "CAKE! The A says its name! Can you say CAKE?",
            "audio_url": "https://example.com/audio/cake.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 300},
                {"viseme": "open", "start_ms": 300, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_bike",
            "phoneme": "bike",
            "prompt": "BIKE! The I says its name! Can you say BIKE?",
            "audio_url": "https://example.com/audio/bike.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 450},
                {"viseme": "rest", "start_ms": 450, "end_ms": 600},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_rope",
            "phoneme": "rope",
            "prompt": "ROPE! The O says its name! Can you say ROPE?",
            "audio_url": "https://example.com/audio/rope.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "round", "start_ms": 250, "end_ms": 450},
                {"viseme": "rest", "start_ms": 450, "end_ms": 600},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_cute",
            "phoneme": "cute",
            "prompt": "CUTE! The U says its name! Can you say CUTE?",
            "audio_url": "https://example.com/audio/cute.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "round", "start_ms": 250, "end_ms": 450},
                {"viseme": "rest", "start_ms": 450, "end_ms": 600},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_pete",
            "phoneme": "Pete",
            "prompt": "PETE! The E says its name! Can you say PETE?",
            "audio_url": "https://example.com/audio/pete.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 450},
                {"viseme": "rest", "start_ms": 450, "end_ms": 600},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # CVC Words - Short A Family
        {
            "id": "lesson_bat",
            "phoneme": "bat",
            "prompt": "B-A-T spells BAT! A flying bat! Say BAT!",
            "audio_url": "https://example.com/audio/bat.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "open", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_mat",
            "phoneme": "mat",
            "prompt": "M-A-T spells MAT! A cozy mat! Say MAT!",
            "audio_url": "https://example.com/audio/mat.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "open", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_hat",
            "phoneme": "hat",
            "prompt": "H-A-T spells HAT! A fun hat! Say HAT!",
            "audio_url": "https://example.com/audio/hat.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "open", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_rat",
            "phoneme": "rat",
            "prompt": "R-A-T spells RAT! A little rat! Say RAT!",
            "audio_url": "https://example.com/audio/rat.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "open", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # CVC Words - Short E Family
        {
            "id": "lesson_bed",
            "phoneme": "bed",
            "prompt": "B-E-D spells BED! Time for bed! Say BED!",
            "audio_url": "https://example.com/audio/bed.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_red",
            "phoneme": "red",
            "prompt": "R-E-D spells RED! A red color! Say RED!",
            "audio_url": "https://example.com/audio/red.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_pet",
            "phoneme": "pet",
            "prompt": "P-E-T spells PET! A cute pet! Say PET!",
            "audio_url": "https://example.com/audio/pet.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # CVC Words - Short I Family
        {
            "id": "lesson_pig",
            "phoneme": "pig",
            "prompt": "P-I-G spells PIG! A pink pig! Say PIG!",
            "audio_url": "https://example.com/audio/pig.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_big",
            "phoneme": "big",
            "prompt": "B-I-G spells BIG! Something big! Say BIG!",
            "audio_url": "https://example.com/audio/big.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_sit",
            "phoneme": "sit",
            "prompt": "S-I-T spells SIT! Sit down! Say SIT!",
            "audio_url": "https://example.com/audio/sit.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # CVC Words - Short O Family
        {
            "id": "lesson_pot",
            "phoneme": "pot",
            "prompt": "P-O-T spells POT! A cooking pot! Say POT!",
            "audio_url": "https://example.com/audio/pot.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "round", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_hot",
            "phoneme": "hot",
            "prompt": "H-O-T spells HOT! Very hot! Say HOT!",
            "audio_url": "https://example.com/audio/hot.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "round", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # Vowel Teams
        {
            "id": "lesson_rain",
            "phoneme": "rain",
            "prompt": "RAIN! AI says A! Can you say RAIN?",
            "audio_url": "https://example.com/audio/rain.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "open", "start_ms": 250, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_play",
            "phoneme": "play",
            "prompt": "PLAY! AY says A! Let's play! Say PLAY!",
            "audio_url": "https://example.com/audio/play.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "open", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_see",
            "phoneme": "see",
            "prompt": "SEE! EE says E! I can see! Say SEE!",
            "audio_url": "https://example.com/audio/see.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 450},
                {"viseme": "rest", "start_ms": 450, "end_ms": 600},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_read",
            "phoneme": "read",
            "prompt": "READ! EA says E! Let's read! Say READ!",
            "audio_url": "https://example.com/audio/read.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 450},
                {"viseme": "open", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_boat",
            "phoneme": "boat",
            "prompt": "BOAT! OA says O! A boat floats! Say BOAT!",
            "audio_url": "https://example.com/audio/boat.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 250},
                {"viseme": "round", "start_ms": 250, "end_ms": 450},
                {"viseme": "open", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_snow",
            "phoneme": "snow",
            "prompt": "SNOW! OW says O! White snow! Say SNOW!",
            "audio_url": "https://example.com/audio/snow.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "round", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_book",
            "phoneme": "book",
            "prompt": "BOOK! Short OO sound! Read a book! Say BOOK!",
            "audio_url": "https://example.com/audio/book.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 250},
                {"viseme": "round", "start_ms": 250, "end_ms": 400},
                {"viseme": "open", "start_ms": 400, "end_ms": 550},
                {"viseme": "rest", "start_ms": 550, "end_ms": 700},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_moon",
            "phoneme": "moon",
            "prompt": "MOON! Long OO sound! See the moon! Say MOON!",
            "audio_url": "https://example.com/audio/moon.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "round", "start_ms": 200, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # R-Controlled Vowels
        {
            "id": "lesson_car",
            "phoneme": "car",
            "prompt": "CAR! AR says AR! Vroom vroom car! Say CAR!",
            "audio_url": "https://example.com/audio/car.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "open", "start_ms": 250, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_her",
            "phoneme": "her",
            "prompt": "HER! ER says ER! This is her! Say HER!",
            "audio_url": "https://example.com/audio/her.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 400},
                {"viseme": "smile", "start_ms": 400, "end_ms": 550},
                {"viseme": "rest", "start_ms": 550, "end_ms": 700},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_bird",
            "phoneme": "bird",
            "prompt": "BIRD! IR says ER! A flying bird! Say BIRD!",
            "audio_url": "https://example.com/audio/bird.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 400},
                {"viseme": "smile", "start_ms": 400, "end_ms": 550},
                {"viseme": "open", "start_ms": 550, "end_ms": 700},
                {"viseme": "rest", "start_ms": 700, "end_ms": 850},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_for",
            "phoneme": "for",
            "prompt": "FOR! OR says OR! This is for you! Say FOR!",
            "audio_url": "https://example.com/audio/for.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "round", "start_ms": 200, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_fur",
            "phoneme": "fur",
            "prompt": "FUR! UR says ER! Soft fur! Say FUR!",
            "audio_url": "https://example.com/audio/fur.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 400},
                {"viseme": "smile", "start_ms": 400, "end_ms": 550},
                {"viseme": "rest", "start_ms": 550, "end_ms": 700},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # Beginning Blends
        {
            "id": "lesson_blue",
            "phoneme": "blue",
            "prompt": "BLUE! BL blend! The sky is blue! Say BLUE!",
            "audio_url": "https://example.com/audio/blue.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 350},
                {"viseme": "round", "start_ms": 350, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_clap",
            "phoneme": "clap",
            "prompt": "CLAP! CL blend! Clap your hands! Say CLAP!",
            "audio_url": "https://example.com/audio/clap.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "open", "start_ms": 300, "end_ms": 450},
                {"viseme": "round", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_flag",
            "phoneme": "flag",
            "prompt": "FLAG! FL blend! Wave the flag! Say FLAG!",
            "audio_url": "https://example.com/audio/flag.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "open", "start_ms": 300, "end_ms": 450},
                {"viseme": "open", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_brown",
            "phoneme": "brown",
            "prompt": "BROWN! BR blend! A brown bear! Say BROWN!",
            "audio_url": "https://example.com/audio/brown.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "round", "start_ms": 300, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_crab",
            "phoneme": "crab",
            "prompt": "CRAB! CR blend! A crunchy crab! Say CRAB!",
            "audio_url": "https://example.com/audio/crab.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "open", "start_ms": 300, "end_ms": 450},
                {"viseme": "round", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_drum",
            "phoneme": "drum",
            "prompt": "DRUM! DR blend! Bang the drum! Say DRUM!",
            "audio_url": "https://example.com/audio/drum.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "round", "start_ms": 300, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_frog",
            "phoneme": "frog",
            "prompt": "FROG! FR blend! A jumping frog! Say FROG!",
            "audio_url": "https://example.com/audio/frog.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "round", "start_ms": 300, "end_ms": 450},
                {"viseme": "open", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_green",
            "phoneme": "green",
            "prompt": "GREEN! GR blend! Green grass! Say GREEN!",
            "audio_url": "https://example.com/audio/green.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "smile", "start_ms": 300, "end_ms": 500},
                {"viseme": "smile", "start_ms": 500, "end_ms": 650},
                {"viseme": "rest", "start_ms": 650, "end_ms": 800},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_print",
            "phoneme": "print",
            "prompt": "PRINT! PR blend! Print a picture! Say PRINT!",
            "audio_url": "https://example.com/audio/print.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "round", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "smile", "start_ms": 300, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "open", "start_ms": 600, "end_ms": 750},
                {"viseme": "rest", "start_ms": 750, "end_ms": 900},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_tree",
            "phoneme": "tree",
            "prompt": "TREE! TR blend! A tall tree! Say TREE!",
            "audio_url": "https://example.com/audio/tree.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 200},
                {"viseme": "smile", "start_ms": 200, "end_ms": 300},
                {"viseme": "smile", "start_ms": 300, "end_ms": 500},
                {"viseme": "rest", "start_ms": 500, "end_ms": 650},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_stop",
            "phoneme": "stop",
            "prompt": "STOP! ST blend! Stop right there! Say STOP!",
            "audio_url": "https://example.com/audio/stop.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "open", "start_ms": 200, "end_ms": 300},
                {"viseme": "round", "start_ms": 300, "end_ms": 450},
                {"viseme": "round", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_spin",
            "phoneme": "spin",
            "prompt": "SPIN! SP blend! Spin around! Say SPIN!",
            "audio_url": "https://example.com/audio/spin.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 200},
                {"viseme": "round", "start_ms": 200, "end_ms": 300},
                {"viseme": "smile", "start_ms": 300, "end_ms": 450},
                {"viseme": "smile", "start_ms": 450, "end_ms": 600},
                {"viseme": "rest", "start_ms": 600, "end_ms": 750},
            ],
            "difficulty": 3,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        # Common Sight Words
        {
            "id": "lesson_the",
            "phoneme": "the",
            "prompt": "THE! The most common word! Say THE!",
            "audio_url": "https://example.com/audio/the.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_and",
            "phoneme": "and",
            "prompt": "AND! Connect words with AND! Say AND!",
            "audio_url": "https://example.com/audio/and.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "open", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 400},
                {"viseme": "open", "start_ms": 400, "end_ms": 550},
                {"viseme": "rest", "start_ms": 550, "end_ms": 700},
            ],
            "difficulty": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_is",
            "phoneme": "is",
            "prompt": "IS! This IS fun! Say IS!",
            "audio_url": "https://example.com/audio/is.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_it",
            "phoneme": "it",
            "prompt": "IT! Point to IT! Say IT!",
            "audio_url": "https://example.com/audio/it.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "open", "start_ms": 250, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "lesson_in",
            "phoneme": "in",
            "prompt": "IN! Something IN something! Say IN!",
            "audio_url": "https://example.com/audio/in.mp3",
            "visemes": [
                {"viseme": "rest", "start_ms": 0, "end_ms": 100},
                {"viseme": "smile", "start_ms": 100, "end_ms": 250},
                {"viseme": "smile", "start_ms": 250, "end_ms": 400},
                {"viseme": "rest", "start_ms": 400, "end_ms": 550},
            ],
            "difficulty": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        },
    ]

    @staticmethod
    async def init_sample_lessons():
        """Initialize database with sample lessons (idempotent)"""
        try:
            existing = await db.get_all("lessons")
            if not existing:
                for lesson in LessonService.SAMPLE_LESSONS:
                    await db.insert_one("lessons", lesson)
                print("✓ Initialized sample lessons")
        except Exception as e:
            print(f"✗ Error initializing lessons: {e}")

    @staticmethod
    async def get_random_lesson():
        """Get a random lesson from the database"""
        import random
        lessons = await db.get_all("lessons")
        if not lessons:
            # Initialize database with sample lessons on first call
            for lesson in LessonService.SAMPLE_LESSONS:
                await db.insert_one("lessons", lesson)
            lessons = LessonService.SAMPLE_LESSONS
        return random.choice(lessons)

    @staticmethod
    async def get_lesson_by_phoneme(phoneme: str):
        """Get lesson by phoneme"""
        lessons = await db.get_by_index("lessons", "phoneme", phoneme)
        return lessons[0] if lessons else None

    @staticmethod
    async def get_all_lessons():
        """Get all lessons"""
        lessons = await db.get_all("lessons")
        if not lessons:
            # Initialize database with sample lessons
            for lesson in LessonService.SAMPLE_LESSONS:
                await db.insert_one("lessons", lesson)
            lessons = LessonService.SAMPLE_LESSONS
        return lessons

    @staticmethod
    async def create_lesson(phoneme: str, prompt: str, audio_url: str, visemes: list, difficulty: int = 1):
        """Create a new lesson"""
        lesson_id = f"lesson_{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow().isoformat()
        
        lesson = {
            "id": lesson_id,
            "phoneme": phoneme,
            "prompt": prompt,
            "audio_url": audio_url,
            "visemes": visemes,
            "difficulty": difficulty,
            "created_at": now,
            "updated_at": now,
        }
        
        lesson_id = await db.insert_one("lessons", lesson)
        return await db.get_by_id("lessons", lesson_id)

class ProgressService:
    """Service for user progress tracking"""

    @staticmethod
    async def get_user_progress(user_id: str) -> list:
        """Get all progress records for a user"""
        return await db.get_by_index("user_progress", "user_id", user_id)

    @staticmethod
    async def update_progress(user_id: str, phoneme: str, score: float, passed: bool):
        """Update user progress for a phoneme"""
        progress_list = await db.get_by_index("user_progress", "user_id", user_id)
        
        # Find existing progress for this phoneme
        existing = next((p for p in progress_list if p.get("phoneme") == phoneme), None)
        
        if existing:
            # Update existing
            updates = {
                "attempts": existing.get("attempts", 0) + 1,
                "best_score": max(existing.get("best_score", 0), score),
                "last_attempted": datetime.utcnow().isoformat(),
                "mastered": passed and score >= 0.8,
            }
            await db.update_one("user_progress", existing["id"], updates)
        else:
            # Create new
            progress_id = f"progress_{uuid.uuid4().hex[:8]}"
            progress = {
                "id": progress_id,
                "user_id": user_id,
                "phoneme": phoneme,
                "attempts": 1,
                "best_score": score,
                "last_attempted": datetime.utcnow().isoformat(),
                "mastered": passed and score >= 0.8,
            }
            await db.insert_one("user_progress", progress)

    @staticmethod
    async def get_mastered_phonemes(user_id: str) -> list:
        """Get list of mastered phonemes for a user"""
        progress_list = await db.get_by_index("user_progress", "user_id", user_id)
        return [p["phoneme"] for p in progress_list if p.get("mastered")]

class RecordingService:
    """Service for recording management"""

    @staticmethod
    async def save_recording(user_id: str, lesson_id: str, duration_ms: int, file_path: str):
        """Save recording metadata"""
        recording_id = f"recording_{uuid.uuid4().hex[:8]}"
        
        recording = {
            "id": recording_id,
            "user_id": user_id,
            "lesson_id": lesson_id,
            "duration_ms": duration_ms,
            "file_path": file_path,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        return await db.insert_one("recordings", recording)

    @staticmethod
    async def get_user_recordings(user_id: str):
        """Get all recordings for a user"""
        return await db.get_by_index("recordings", "user_id", user_id)
