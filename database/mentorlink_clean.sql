

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', 'public', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA
--

ALTER SCHEMA public OWNER TO mentorlink_user;

--
-- TYPES ENUM
--

CREATE TYPE public.filiere_enum AS ENUM (
    'IA',
    'IM',
    'GL',
    'SEIoT',
    'SI'
);
ALTER TYPE public.filiere_enum OWNER TO postgres;

CREATE TYPE public.format_annonce_enum AS ENUM (
    'presentiel',
    'en_ligne',
    'les_deux'
);
ALTER TYPE public.format_annonce_enum OWNER TO postgres;

CREATE TYPE public.format_prefere_enum AS ENUM (
    'presentiel',
    'en_ligne',
    'les_deux'
);
ALTER TYPE public.format_prefere_enum OWNER TO postgres;

CREATE TYPE public.jour_enum AS ENUM (
    'Lundi',
    'Mardi',
    'Mercredi',
    'Jeudi',
    'Vendredi',
    'Samedi',
    'Dimanche'
);
ALTER TYPE public.jour_enum OWNER TO postgres;

CREATE TYPE public.niveau_enum AS ENUM (
    'L1',
    'L2',
    'L3',
    'M1',
    'M2'
);
ALTER TYPE public.niveau_enum OWNER TO postgres;

CREATE TYPE public.sexe_enum AS ENUM (
    'M',
    'F'
);
ALTER TYPE public.sexe_enum OWNER TO postgres;

CREATE TYPE public.statut_annonce_enum AS ENUM (
    'active',
    'archivee',
    'fermee'
);
ALTER TYPE public.statut_annonce_enum OWNER TO postgres;

CREATE TYPE public.statut_candidature_enum AS ENUM (
    'en_attente',
    'acceptee',
    'refusee'
);
ALTER TYPE public.statut_candidature_enum OWNER TO postgres;

CREATE TYPE public.statut_matching_enum AS ENUM (
    'propose',
    'accepte',
    'refuse',
    'termine'
);
ALTER TYPE public.statut_matching_enum OWNER TO postgres;

CREATE TYPE public.statut_report_enum AS ENUM (
    'en_attente',
    'traite',
    'rejete'
);
ALTER TYPE public.statut_report_enum OWNER TO postgres;

CREATE TYPE public.statut_user_enum AS ENUM (
    'connecte',
    'deconnecte'
);
ALTER TYPE public.statut_user_enum OWNER TO postgres;

CREATE TYPE public.type_annonce_enum AS ENUM (
    'offre',
    'demande'
);
ALTER TYPE public.type_annonce_enum OWNER TO postgres;

CREATE TYPE public.type_competence_enum AS ENUM (
    'competence',
    'lacune'
);
ALTER TYPE public.type_competence_enum OWNER TO postgres;

CREATE TYPE public.type_notification_enum AS ENUM (
    'message',
    'candidature',
    'matching',
    'systeme',
    'rappel'
);
ALTER TYPE public.type_notification_enum OWNER TO postgres;

--
-- FONCTIONS
--

CREATE FUNCTION public.update_annonce_likes() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE annonce
    SET likes = (
        SELECT COUNT(*) FROM favori_annonce WHERE annonce_id = NEW.annonce_id
    )
    WHERE id = NEW.annonce_id;
    RETURN NEW;
END;
$$;
ALTER FUNCTION public.update_annonce_likes() OWNER TO postgres;

CREATE FUNCTION public.update_user_rating() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE users
    SET rating_moyen = (
        SELECT COALESCE(AVG(f.note), 0)
        FROM feedback f
        JOIN matching m ON f.matching_id = m.id
        WHERE m.mentor_id = users.id OR m.mentore_id = users.id
    ),
    nb_avis = (
        SELECT COUNT(*)
        FROM feedback f
        JOIN matching m ON f.matching_id = m.id
        WHERE m.mentor_id = users.id OR m.mentore_id = users.id
    )
    WHERE id IN (
        SELECT mentor_id  FROM matching WHERE id = NEW.matching_id
        UNION
        SELECT mentore_id FROM matching WHERE id = NEW.matching_id
    );
    RETURN NEW;
END;
$$;
ALTER FUNCTION public.update_user_rating() OWNER TO postgres;

SET default_tablespace = '';
SET default_table_access_method = heap;

--
-- TABLES
--

CREATE TABLE public.annonce (
    id integer NOT NULL,
    auteur_id integer NOT NULL,
    matiere_id integer NOT NULL,
    titre character varying(200) NOT NULL,
    type public.type_annonce_enum NOT NULL,
    format public.format_annonce_enum DEFAULT 'les_deux'::public.format_annonce_enum NOT NULL,
    description text,
    statut public.statut_annonce_enum DEFAULT 'active'::public.statut_annonce_enum NOT NULL,
    places_max integer DEFAULT 1,
    places_restantes integer DEFAULT 1,
    likes integer DEFAULT 0,
    vues integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);
ALTER TABLE public.annonce OWNER TO postgres;

CREATE SEQUENCE public.annonce_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.annonce_id_seq OWNER TO postgres;
ALTER SEQUENCE public.annonce_id_seq OWNED BY public.annonce.id;

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
ALTER TABLE public.auth_group OWNER TO mentorlink_user;
ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
);

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
ALTER TABLE public.auth_group_permissions OWNER TO mentorlink_user;
ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
);

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
ALTER TABLE public.auth_permission OWNER TO mentorlink_user;
ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
);

CREATE TABLE public.candidature (
    id integer NOT NULL,
    annonce_id integer NOT NULL,
    candidat_id integer NOT NULL,
    messages text,
    statut public.statut_candidature_enum DEFAULT 'en_attente'::public.statut_candidature_enum NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);
ALTER TABLE public.candidature OWNER TO postgres;

CREATE SEQUENCE public.candidature_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.candidature_id_seq OWNER TO postgres;
ALTER SEQUENCE public.candidature_id_seq OWNED BY public.candidature.id;

CREATE TABLE public.competence (
    id integer NOT NULL,
    user_id integer NOT NULL,
    matiere_id integer NOT NULL,
    type public.type_competence_enum NOT NULL,
    niveau integer DEFAULT 1,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT competence_niveau_check CHECK (((niveau >= 1) AND (niveau <= 5)))
);
ALTER TABLE public.competence OWNER TO postgres;

CREATE SEQUENCE public.competence_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.competence_id_seq OWNER TO postgres;
ALTER SEQUENCE public.competence_id_seq OWNED BY public.competence.id;

CREATE TABLE public.disponibilite (
    id integer NOT NULL,
    user_id integer NOT NULL,
    jour public.jour_enum NOT NULL,
    heure_debut time without time zone NOT NULL,
    heure_fin time without time zone NOT NULL,
    est_recurrent boolean DEFAULT true,
    CONSTRAINT chk_heures CHECK ((heure_fin > heure_debut))
);
ALTER TABLE public.disponibilite OWNER TO postgres;

CREATE SEQUENCE public.disponibilite_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.disponibilite_id_seq OWNER TO postgres;
ALTER SEQUENCE public.disponibilite_id_seq OWNED BY public.disponibilite.id;

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
ALTER TABLE public.django_admin_log OWNER TO mentorlink_user;
ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
);

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
ALTER TABLE public.django_content_type OWNER TO mentorlink_user;
ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
);

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
ALTER TABLE public.django_migrations OWNER TO mentorlink_user;
ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
);

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
ALTER TABLE public.django_session OWNER TO mentorlink_user;

CREATE TABLE public.favori_annonce (
    id integer NOT NULL,
    user_id integer NOT NULL,
    annonce_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);
ALTER TABLE public.favori_annonce OWNER TO postgres;

CREATE SEQUENCE public.favori_annonce_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.favori_annonce_id_seq OWNER TO postgres;
ALTER SEQUENCE public.favori_annonce_id_seq OWNED BY public.favori_annonce.id;

CREATE TABLE public.feedback (
    id integer NOT NULL,
    matching_id integer NOT NULL,
    auteur_id integer NOT NULL,
    note integer NOT NULL,
    commentaire text,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT feedback_note_check CHECK (((note >= 1) AND (note <= 5)))
);
ALTER TABLE public.feedback OWNER TO postgres;

CREATE SEQUENCE public.feedback_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.feedback_id_seq OWNER TO postgres;
ALTER SEQUENCE public.feedback_id_seq OWNED BY public.feedback.id;

CREATE TABLE public.horaire_hebdo (
    id integer NOT NULL,
    user_id integer NOT NULL,
    jour public.jour_enum NOT NULL,
    heure_debut time without time zone NOT NULL,
    heure_fin time without time zone NOT NULL,
    semaine_debut date,
    semaine_fin date,
    CONSTRAINT chk_heures_horaire CHECK ((heure_fin > heure_debut))
);
ALTER TABLE public.horaire_hebdo OWNER TO postgres;

CREATE SEQUENCE public.horaire_hebdo_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.horaire_hebdo_id_seq OWNER TO postgres;
ALTER SEQUENCE public.horaire_hebdo_id_seq OWNED BY public.horaire_hebdo.id;

CREATE TABLE public.matching (
    id integer NOT NULL,
    mentor_id integer NOT NULL,
    mentore_id integer NOT NULL,
    annonce_id integer,
    score numeric(5,2) NOT NULL,
    statut public.statut_matching_enum DEFAULT 'propose'::public.statut_matching_enum NOT NULL,
    session_date timestamp without time zone,
    duree_minutes integer DEFAULT 60,
    lien_reunion character varying(500),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT chk_no_selfmatch CHECK ((mentor_id <> mentore_id)),
    CONSTRAINT matching_score_check CHECK (((score >= (0)::numeric) AND (score <= (100)::numeric)))
);
ALTER TABLE public.matching OWNER TO postgres;

CREATE SEQUENCE public.matching_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.matching_id_seq OWNER TO postgres;
ALTER SEQUENCE public.matching_id_seq OWNED BY public.matching.id;

CREATE TABLE public.matiere (
    id integer NOT NULL,
    nom character varying(150) NOT NULL,
    categorie character varying(100),
    filiere_cible character varying(100),
    icone character varying(50) DEFAULT 'school'::character varying,
    couleur character varying(20) DEFAULT '#386943'::character varying
);
ALTER TABLE public.matiere OWNER TO postgres;

CREATE SEQUENCE public.matiere_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.matiere_id_seq OWNER TO postgres;
ALTER SEQUENCE public.matiere_id_seq OWNED BY public.matiere.id;

CREATE TABLE public.messages (
    id integer NOT NULL,
    expediteur_id integer NOT NULL,
    destinataire_id integer NOT NULL,
    contenu text NOT NULL,
    lu boolean DEFAULT false NOT NULL,
    lu_at timestamp without time zone,
    message_reply_to integer,
    matching_id integer,
    annonce_id integer,
    est_modifie boolean DEFAULT false,
    est_supprime boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT chk_msg_self CHECK ((expediteur_id <> destinataire_id))
);
ALTER TABLE public.messages OWNER TO postgres;

CREATE SEQUENCE public.messages_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.messages_id_seq OWNER TO postgres;
ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    type public.type_notification_enum NOT NULL,
    titre character varying(200) NOT NULL,
    contenu text,
    lien character varying(500),
    est_lue boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    data_json jsonb
);
ALTER TABLE public.notifications OWNER TO postgres;

CREATE SEQUENCE public.notifications_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.notifications_id_seq OWNER TO postgres;
ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;

CREATE TABLE public.piece_jointe (
    id integer NOT NULL,
    message_id integer NOT NULL,
    nom_fichier character varying(255) NOT NULL,
    url_fichier character varying(500) NOT NULL,
    type_fichier character varying(50),
    taille integer,
    created_at timestamp without time zone DEFAULT now()
);
ALTER TABLE public.piece_jointe OWNER TO postgres;

CREATE SEQUENCE public.piece_jointe_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.piece_jointe_id_seq OWNER TO postgres;
ALTER SEQUENCE public.piece_jointe_id_seq OWNED BY public.piece_jointe.id;

CREATE TABLE public.profil (
    id integer NOT NULL,
    user_id integer NOT NULL,
    filiere public.filiere_enum NOT NULL,
    niveau public.niveau_enum NOT NULL,
    bio text,
    photo_url character varying(500),
    banner_url character varying(500),
    format_prefere public.format_prefere_enum DEFAULT 'les_deux'::public.format_prefere_enum NOT NULL,
    response_rate integer DEFAULT 0,
    avg_response_time integer DEFAULT 0,
    total_sessions integer DEFAULT 0,
    total_heures integer DEFAULT 0,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);
ALTER TABLE public.profil OWNER TO postgres;

CREATE SEQUENCE public.profil_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.profil_id_seq OWNER TO postgres;
ALTER SEQUENCE public.profil_id_seq OWNED BY public.profil.id;

CREATE TABLE public.reaction_message (
    id integer NOT NULL,
    message_id integer NOT NULL,
    user_id integer NOT NULL,
    emoji character varying(10) NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);
ALTER TABLE public.reaction_message OWNER TO postgres;

CREATE SEQUENCE public.reaction_message_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.reaction_message_id_seq OWNER TO postgres;
ALTER SEQUENCE public.reaction_message_id_seq OWNED BY public.reaction_message.id;

CREATE TABLE public.report (
    id integer NOT NULL,
    rapporteur_id integer NOT NULL,
    signale_id integer NOT NULL,
    message_id integer,
    annonce_id integer,
    raison text NOT NULL,
    statut public.statut_report_enum DEFAULT 'en_attente'::public.statut_report_enum,
    created_at timestamp without time zone DEFAULT now(),
    traite_le timestamp without time zone,
    traite_par integer
);
ALTER TABLE public.report OWNER TO postgres;

CREATE SEQUENCE public.report_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.report_id_seq OWNER TO postgres;
ALTER SEQUENCE public.report_id_seq OWNED BY public.report.id;

CREATE TABLE public.users (
    id integer NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    telephone character varying(20) NOT NULL,
    matricule character varying(50),
    password character varying(255) NOT NULL,
    statut public.statut_user_enum DEFAULT 'deconnecte'::public.statut_user_enum NOT NULL,
    sexe public.sexe_enum NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    rating_moyen numeric(3,2) DEFAULT 0,
    nb_avis integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    last_login timestamp without time zone,
    last_seen timestamp without time zone,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    is_superuser boolean DEFAULT false,
    is_staff boolean DEFAULT false,
    username character varying(150) NOT NULL,
    date_joined timestamp without time zone DEFAULT now(),
    groups text,
    user_permissions text,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL
);
ALTER TABLE public.users OWNER TO postgres;

CREATE SEQUENCE public.users_id_seq
    AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.users_id_seq OWNER TO postgres;
ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

--
-- VUE v_score_matching
--

CREATE VIEW public.v_score_matching AS
 SELECT c_mentor.user_id AS mentor_id,
    c_mentore.user_id AS mentore_id,
    count(c_mentor.matiere_id) AS nb_matieres_communes,
    LEAST(round((((count(c_mentor.matiere_id))::numeric / (GREATEST(( SELECT count(*) AS count
           FROM public.competence
          WHERE ((competence.user_id = c_mentore.user_id) AND (competence.type = 'lacune'::public.type_competence_enum))), (1)::bigint))::numeric) * (100)::numeric), 2), (100)::numeric) AS score_matieres
   FROM (public.competence c_mentor
     JOIN public.competence c_mentore ON (((c_mentor.matiere_id = c_mentore.matiere_id) AND (c_mentor.type = 'competence'::public.type_competence_enum) AND (c_mentore.type = 'lacune'::public.type_competence_enum) AND (c_mentor.user_id <> c_mentore.user_id))))
  WHERE ((( SELECT count(*) AS count
           FROM public.competence
          WHERE ((competence.user_id = c_mentor.user_id) AND (competence.type = 'competence'::public.type_competence_enum))) > 0) AND (( SELECT count(*) AS count
           FROM public.competence
          WHERE ((competence.user_id = c_mentore.user_id) AND (competence.type = 'lacune'::public.type_competence_enum))) > 0) AND (EXISTS ( SELECT 1
           FROM public.profil
          WHERE (profil.user_id = c_mentor.user_id))) AND (EXISTS ( SELECT 1
           FROM public.profil
          WHERE (profil.user_id = c_mentore.user_id))) AND (EXISTS ( SELECT 1
           FROM public.disponibilite
          WHERE (disponibilite.user_id = c_mentor.user_id))) AND (EXISTS ( SELECT 1
           FROM public.disponibilite
          WHERE (disponibilite.user_id = c_mentore.user_id))))
  GROUP BY c_mentor.user_id, c_mentore.user_id
 HAVING (count(c_mentor.matiere_id) > 0);
ALTER VIEW public.v_score_matching OWNER TO postgres;

--
-- DEFAULT COLUMN VALUES
--

ALTER TABLE ONLY public.annonce ALTER COLUMN id SET DEFAULT nextval('public.annonce_id_seq'::regclass);
ALTER TABLE ONLY public.candidature ALTER COLUMN id SET DEFAULT nextval('public.candidature_id_seq'::regclass);
ALTER TABLE ONLY public.competence ALTER COLUMN id SET DEFAULT nextval('public.competence_id_seq'::regclass);
ALTER TABLE ONLY public.disponibilite ALTER COLUMN id SET DEFAULT nextval('public.disponibilite_id_seq'::regclass);
ALTER TABLE ONLY public.favori_annonce ALTER COLUMN id SET DEFAULT nextval('public.favori_annonce_id_seq'::regclass);
ALTER TABLE ONLY public.feedback ALTER COLUMN id SET DEFAULT nextval('public.feedback_id_seq'::regclass);
ALTER TABLE ONLY public.horaire_hebdo ALTER COLUMN id SET DEFAULT nextval('public.horaire_hebdo_id_seq'::regclass);
ALTER TABLE ONLY public.matching ALTER COLUMN id SET DEFAULT nextval('public.matching_id_seq'::regclass);
ALTER TABLE ONLY public.matiere ALTER COLUMN id SET DEFAULT nextval('public.matiere_id_seq'::regclass);
ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);
ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
ALTER TABLE ONLY public.piece_jointe ALTER COLUMN id SET DEFAULT nextval('public.piece_jointe_id_seq'::regclass);
ALTER TABLE ONLY public.profil ALTER COLUMN id SET DEFAULT nextval('public.profil_id_seq'::regclass);
ALTER TABLE ONLY public.reaction_message ALTER COLUMN id SET DEFAULT nextval('public.reaction_message_id_seq'::regclass);
ALTER TABLE ONLY public.report ALTER COLUMN id SET DEFAULT nextval('public.report_id_seq'::regclass);
ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

--
-- DATA — Django internal tables (nécessaires au fonctionnement de Flask/Django)
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	core	annonce
7	core	matiere
8	users	disponibilite
9	users	profil
10	users	users
11	feed	candidature
12	feed	favoriannonce
13	matching	competence
14	matching	feedback
15	matching	matching
16	messaging	messages
17	messaging	piecejointe
18	messaging	reactionmessage
\.

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-06-10 10:26:57.7521+01
2	admin	0001_initial	2026-06-10 10:26:57.795678+01
3	admin	0002_logentry_remove_auto_add	2026-06-10 10:26:57.809981+01
4	admin	0003_logentry_add_action_flag_choices	2026-06-10 10:26:57.8296+01
5	contenttypes	0002_remove_content_type_name	2026-06-10 10:26:57.878784+01
6	auth	0001_initial	2026-06-10 10:26:57.962642+01
7	auth	0002_alter_permission_name_max_length	2026-06-10 10:26:57.992486+01
8	auth	0003_alter_user_email_max_length	2026-06-10 10:26:58.018311+01
9	auth	0004_alter_user_username_opts	2026-06-10 10:26:58.039122+01
10	auth	0005_alter_user_last_login_null	2026-06-10 10:26:58.052497+01
11	auth	0006_require_contenttypes_0002	2026-06-10 10:26:58.062743+01
12	auth	0007_alter_validators_add_error_messages	2026-06-10 10:26:58.081174+01
13	auth	0008_alter_user_username_max_length	2026-06-10 10:26:58.096283+01
14	auth	0009_alter_user_last_name_max_length	2026-06-10 10:26:58.112234+01
15	auth	0010_alter_group_name_max_length	2026-06-10 10:26:58.134005+01
16	auth	0011_update_proxy_permissions	2026-06-10 10:26:58.166385+01
17	auth	0012_alter_user_first_name_max_length	2026-06-10 10:26:58.178512+01
18	sessions	0001_initial	2026-06-10 10:26:58.212853+01
\.

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add matiere	7	add_matiere
22	Can change matiere	7	change_matiere
23	Can delete matiere	7	delete_matiere
24	Can view matiere	7	view_matiere
25	Can add annonce	6	add_annonce
26	Can change annonce	6	change_annonce
27	Can delete annonce	6	delete_annonce
28	Can view annonce	6	view_annonce
29	Can add users	10	add_users
30	Can change users	10	change_users
31	Can delete users	10	delete_users
32	Can view users	10	view_users
33	Can add profil	9	add_profil
34	Can change profil	9	change_profil
35	Can delete profil	9	delete_profil
36	Can view profil	9	view_profil
37	Can add disponibilite	8	add_disponibilite
38	Can change disponibilite	8	change_disponibilite
39	Can delete disponibilite	8	delete_disponibilite
40	Can view disponibilite	8	view_disponibilite
41	Can add candidature	11	add_candidature
42	Can change candidature	11	change_candidature
43	Can delete candidature	11	delete_candidature
44	Can view candidature	11	view_candidature
45	Can add favori annonce	12	add_favoriannonce
46	Can change favori annonce	12	change_favoriannonce
47	Can delete favori annonce	12	delete_favoriannonce
48	Can view favori annonce	12	view_favoriannonce
49	Can add competence	13	add_competence
50	Can change competence	13	change_competence
51	Can delete competence	13	delete_competence
52	Can view competence	13	view_competence
53	Can add matching	15	add_matching
54	Can change matching	15	change_matching
55	Can delete matching	15	delete_matching
56	Can view matching	15	view_matching
57	Can add feedback	14	add_feedback
58	Can change feedback	14	change_feedback
59	Can delete feedback	14	delete_feedback
60	Can view feedback	14	view_feedback
61	Can add messages	16	add_messages
62	Can change messages	16	change_messages
63	Can delete messages	16	delete_messages
64	Can view messages	16	view_messages
65	Can add piece jointe	17	add_piecejointe
66	Can change piece jointe	17	change_piecejointe
67	Can delete piece jointe	17	delete_piecejointe
68	Can view piece jointe	17	view_piecejointe
69	Can add reaction message	18	add_reactionmessage
70	Can change reaction message	18	change_reactionmessage
71	Can delete reaction message	18	delete_reactionmessage
72	Can view reaction message	18	view_reactionmessage
\.

--
-- DATA — Matières de référence (données fixes nécessaires à l'application)
--

COPY public.matiere (id, nom, categorie, filiere_cible, icone, couleur) FROM stdin;
1	Logique arithmetique	Mathematiques	Toutes	calculate	#386943
2	Algebre lineaire	Mathematiques	Toutes	functions	#386943
3	Analyse et applications	Mathematiques	Toutes	timeline	#386943
4	Probabilites et statistiques	Mathematiques	Toutes	bar_chart	#386943
5	Algorithmique	Informatique	Toutes	code	#006a68
6	Programmation Python	Informatique	Toutes	terminal	#006a68
7	Langage C	Informatique	Toutes	data_usage	#006a68
10	Machine Learning	Informatique	Toutes	neurology	#36675a
12	Anglais technique	Langue	Toutes	translate	#386943
13	Bases de données SQL	Informatique	Toutes	database	#386943
14	Développement Web	Informatique	Toutes	language	#386943
15	Mathématiques	Mathématiques	Toutes	calculate	#386943
16	Statistiques	Mathématiques	Toutes	bar_chart	#386943
17	Réseaux informatiques	Informatique	Toutes	router	#386943
18	Cybersécurité	Informatique	Toutes	security	#386943
\.

--
-- SEQUENCES — valeurs initiales (IDs commencent à 1 pour toutes les tables utilisateur)
--

SELECT pg_catalog.setval('public.annonce_id_seq', 1, false);
SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
SELECT pg_catalog.setval('public.auth_permission_id_seq', 72, true);
SELECT pg_catalog.setval('public.candidature_id_seq', 1, false);
SELECT pg_catalog.setval('public.competence_id_seq', 1, false);
SELECT pg_catalog.setval('public.disponibilite_id_seq', 1, false);
SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);
SELECT pg_catalog.setval('public.django_content_type_id_seq', 18, true);
SELECT pg_catalog.setval('public.django_migrations_id_seq', 18, true);
SELECT pg_catalog.setval('public.favori_annonce_id_seq', 1, false);
SELECT pg_catalog.setval('public.feedback_id_seq', 1, false);
SELECT pg_catalog.setval('public.horaire_hebdo_id_seq', 1, false);
SELECT pg_catalog.setval('public.matching_id_seq', 1, false);
SELECT pg_catalog.setval('public.matiere_id_seq', 18, true);
SELECT pg_catalog.setval('public.messages_id_seq', 1, false);
SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);
SELECT pg_catalog.setval('public.piece_jointe_id_seq', 1, false);
SELECT pg_catalog.setval('public.profil_id_seq', 1, false);
SELECT pg_catalog.setval('public.reaction_message_id_seq', 1, false);
SELECT pg_catalog.setval('public.report_id_seq', 1, false);
SELECT pg_catalog.setval('public.users_id_seq', 1, false);

--
-- CONTRAINTES PRIMARY KEY
--

ALTER TABLE ONLY public.annonce ADD CONSTRAINT annonce_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group ADD CONSTRAINT auth_group_name_key UNIQUE (name);
ALTER TABLE ONLY public.auth_group_permissions ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
ALTER TABLE ONLY public.auth_group_permissions ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_permission ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
ALTER TABLE ONLY public.auth_permission ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.candidature ADD CONSTRAINT candidature_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.competence ADD CONSTRAINT competence_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.disponibilite ADD CONSTRAINT disponibilite_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_admin_log ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_content_type ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
ALTER TABLE ONLY public.django_content_type ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_migrations ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_session ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
ALTER TABLE ONLY public.favori_annonce ADD CONSTRAINT favori_annonce_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.feedback ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.horaire_hebdo ADD CONSTRAINT horaire_hebdo_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.matching ADD CONSTRAINT matching_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.matiere ADD CONSTRAINT matiere_nom_key UNIQUE (nom);
ALTER TABLE ONLY public.matiere ADD CONSTRAINT matiere_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.messages ADD CONSTRAINT messages_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.notifications ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.piece_jointe ADD CONSTRAINT piece_jointe_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_user_id_key UNIQUE (user_id);
ALTER TABLE ONLY public.reaction_message ADD CONSTRAINT reaction_message_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.report ADD CONSTRAINT report_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.candidature ADD CONSTRAINT uq_candidature UNIQUE (annonce_id, candidat_id);
ALTER TABLE ONLY public.competence ADD CONSTRAINT uq_competence_user_matiere UNIQUE (user_id, matiere_id);
ALTER TABLE ONLY public.favori_annonce ADD CONSTRAINT uq_favori UNIQUE (user_id, annonce_id);
ALTER TABLE ONLY public.feedback ADD CONSTRAINT uq_feedback UNIQUE (matching_id, auteur_id);
ALTER TABLE ONLY public.matching ADD CONSTRAINT uq_matching UNIQUE (mentor_id, mentore_id, annonce_id);
ALTER TABLE ONLY public.reaction_message ADD CONSTRAINT uq_reaction UNIQUE (message_id, user_id, emoji);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_email_key UNIQUE (email);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_matricule_key UNIQUE (matricule);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_telephone_key UNIQUE (telephone);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_username_key UNIQUE (username);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_username_unique UNIQUE (username);

--
-- INDEX
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
CREATE INDEX idx_annonce_auteur ON public.annonce USING btree (auteur_id, statut);
CREATE INDEX idx_annonce_matiere ON public.annonce USING btree (matiere_id);
CREATE INDEX idx_annonce_statut ON public.annonce USING btree (statut, created_at DESC);
CREATE INDEX idx_candidature_annonce ON public.candidature USING btree (annonce_id, statut);
CREATE INDEX idx_candidature_candidat ON public.candidature USING btree (candidat_id);
CREATE INDEX idx_competence_matiere ON public.competence USING btree (matiere_id, type);
CREATE INDEX idx_competence_user ON public.competence USING btree (user_id, type);
CREATE INDEX idx_dispo_user ON public.disponibilite USING btree (user_id, jour);
CREATE INDEX idx_feedback_auteur ON public.feedback USING btree (auteur_id);
CREATE INDEX idx_feedback_matching ON public.feedback USING btree (matching_id);
CREATE INDEX idx_horaire_user ON public.horaire_hebdo USING btree (user_id, jour);
CREATE INDEX idx_matching_mentor ON public.matching USING btree (mentor_id, statut);
CREATE INDEX idx_matching_mentore ON public.matching USING btree (mentore_id, statut);
CREATE INDEX idx_matching_score ON public.matching USING btree (score DESC);
CREATE INDEX idx_message_conv ON public.messages USING btree (expediteur_id, destinataire_id, created_at);
CREATE INDEX idx_message_match ON public.messages USING btree (matching_id);
CREATE INDEX idx_message_non_lus ON public.messages USING btree (destinataire_id, lu) WHERE (lu = false);
CREATE INDEX idx_notif_user ON public.notifications USING btree (user_id, est_lue, created_at DESC);

--
-- TRIGGERS
--

CREATE TRIGGER trigger_update_likes AFTER INSERT OR DELETE ON public.favori_annonce FOR EACH ROW EXECUTE FUNCTION public.update_annonce_likes();
CREATE TRIGGER trigger_update_rating AFTER INSERT ON public.feedback FOR EACH ROW EXECUTE FUNCTION public.update_user_rating();

--
-- FOREIGN KEYS
--

ALTER TABLE ONLY public.annonce ADD CONSTRAINT annonce_auteur_id_fkey FOREIGN KEY (auteur_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.annonce ADD CONSTRAINT annonce_matiere_id_fkey FOREIGN KEY (matiere_id) REFERENCES public.matiere(id) ON DELETE RESTRICT;
ALTER TABLE ONLY public.auth_group_permissions ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_group_permissions ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_permission ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.candidature ADD CONSTRAINT candidature_annonce_id_fkey FOREIGN KEY (annonce_id) REFERENCES public.annonce(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.candidature ADD CONSTRAINT candidature_candidat_id_fkey FOREIGN KEY (candidat_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.competence ADD CONSTRAINT competence_matiere_id_fkey FOREIGN KEY (matiere_id) REFERENCES public.matiere(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.competence ADD CONSTRAINT competence_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.disponibilite ADD CONSTRAINT disponibilite_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.django_admin_log ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.favori_annonce ADD CONSTRAINT favori_annonce_annonce_id_fkey FOREIGN KEY (annonce_id) REFERENCES public.annonce(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.favori_annonce ADD CONSTRAINT favori_annonce_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.feedback ADD CONSTRAINT feedback_auteur_id_fkey FOREIGN KEY (auteur_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.feedback ADD CONSTRAINT feedback_matching_id_fkey FOREIGN KEY (matching_id) REFERENCES public.matching(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.horaire_hebdo ADD CONSTRAINT horaire_hebdo_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.matching ADD CONSTRAINT matching_annonce_id_fkey FOREIGN KEY (annonce_id) REFERENCES public.annonce(id) ON DELETE SET NULL;
ALTER TABLE ONLY public.matching ADD CONSTRAINT matching_mentor_id_fkey FOREIGN KEY (mentor_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.matching ADD CONSTRAINT matching_mentore_id_fkey FOREIGN KEY (mentore_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.messages ADD CONSTRAINT messages_annonce_id_fkey FOREIGN KEY (annonce_id) REFERENCES public.annonce(id) ON DELETE SET NULL;
ALTER TABLE ONLY public.messages ADD CONSTRAINT messages_destinataire_id_fkey FOREIGN KEY (destinataire_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.messages ADD CONSTRAINT messages_expediteur_id_fkey FOREIGN KEY (expediteur_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.messages ADD CONSTRAINT messages_matching_id_fkey FOREIGN KEY (matching_id) REFERENCES public.matching(id) ON DELETE SET NULL;
ALTER TABLE ONLY public.messages ADD CONSTRAINT messages_message_reply_to_fkey FOREIGN KEY (message_reply_to) REFERENCES public.messages(id) ON DELETE SET NULL;
ALTER TABLE ONLY public.notifications ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.piece_jointe ADD CONSTRAINT piece_jointe_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.messages(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.profil ADD CONSTRAINT profil_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.reaction_message ADD CONSTRAINT reaction_message_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.messages(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.reaction_message ADD CONSTRAINT reaction_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.report ADD CONSTRAINT report_annonce_id_fkey FOREIGN KEY (annonce_id) REFERENCES public.annonce(id) ON DELETE SET NULL;
ALTER TABLE ONLY public.report ADD CONSTRAINT report_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.messages(id) ON DELETE SET NULL;
ALTER TABLE ONLY public.report ADD CONSTRAINT report_rapporteur_id_fkey FOREIGN KEY (rapporteur_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.report ADD CONSTRAINT report_signale_id_fkey FOREIGN KEY (signale_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.report ADD CONSTRAINT report_traite_par_fkey FOREIGN KEY (traite_par) REFERENCES public.users(id) ON DELETE SET NULL;

--
-- ACL (GRANTS)
--

GRANT ALL ON FUNCTION public.update_annonce_likes() TO mentorlink_user;
GRANT ALL ON FUNCTION public.update_user_rating() TO mentorlink_user;
GRANT ALL ON TABLE public.annonce TO mentorlink_user;
GRANT ALL ON SEQUENCE public.annonce_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.candidature TO mentorlink_user;
GRANT ALL ON SEQUENCE public.candidature_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.competence TO mentorlink_user;
GRANT ALL ON SEQUENCE public.competence_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.disponibilite TO mentorlink_user;
GRANT ALL ON SEQUENCE public.disponibilite_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.favori_annonce TO mentorlink_user;
GRANT ALL ON SEQUENCE public.favori_annonce_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.feedback TO mentorlink_user;
GRANT ALL ON SEQUENCE public.feedback_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.horaire_hebdo TO mentorlink_user;
GRANT ALL ON SEQUENCE public.horaire_hebdo_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.matching TO mentorlink_user;
GRANT ALL ON SEQUENCE public.matching_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.matiere TO mentorlink_user;
GRANT ALL ON SEQUENCE public.matiere_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.messages TO mentorlink_user;
GRANT ALL ON SEQUENCE public.messages_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.notifications TO mentorlink_user;
GRANT ALL ON SEQUENCE public.notifications_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.piece_jointe TO mentorlink_user;
GRANT ALL ON SEQUENCE public.piece_jointe_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.profil TO mentorlink_user;
GRANT ALL ON SEQUENCE public.profil_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.reaction_message TO mentorlink_user;
GRANT ALL ON SEQUENCE public.reaction_message_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.report TO mentorlink_user;
GRANT ALL ON SEQUENCE public.report_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.users TO mentorlink_user;
GRANT ALL ON SEQUENCE public.users_id_seq TO mentorlink_user;
GRANT ALL ON TABLE public.v_score_matching TO mentorlink_user;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO mentorlink_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO mentorlink_user;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO mentorlink_user;

--
-- PostgreSQL database dump complete
--
