--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-11-18 07:24:54

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16553)
-- Name: freelancer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.freelancer (
    freelancer_id integer NOT NULL,
    name character varying,
    email character varying,
    rating character varying
);


ALTER TABLE public.freelancer OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16622)
-- Name: freelancer_skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.freelancer_skill (
    freelancer_skill_id integer NOT NULL,
    freelancer_id integer NOT NULL,
    skill_id integer NOT NULL,
    skill_level character varying
);


ALTER TABLE public.freelancer_skill OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16560)
-- Name: project; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project (
    project_id integer NOT NULL,
    name character varying,
    creation_time timestamp without time zone NOT NULL,
    status character varying
);


ALTER TABLE public.project OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16598)
-- Name: skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill (
    skill_id integer NOT NULL,
    name character varying,
    field character varying
);


ALTER TABLE public.skill OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16581)
-- Name: task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task (
    task_id integer NOT NULL,
    description character varying,
    deadline timestamp without time zone,
    project_id integer NOT NULL,
    freelancer_id integer
);


ALTER TABLE public.task OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16605)
-- Name: task_skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_skill (
    task_skill_id integer NOT NULL,
    task_id integer NOT NULL,
    skill_id integer NOT NULL,
    required_level character varying
);


ALTER TABLE public.task_skill OWNER TO postgres;

--
-- TOC entry 4868 (class 0 OID 16553)
-- Dependencies: 215
-- Data for Name: freelancer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.freelancer (freelancer_id, name, email, rating) FROM stdin;
1	Roberto	123@email.com	5/5
2	Carl	1234@email.com	4/5
\.


--
-- TOC entry 4873 (class 0 OID 16622)
-- Dependencies: 220
-- Data for Name: freelancer_skill; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.freelancer_skill (freelancer_skill_id, freelancer_id, skill_id, skill_level) FROM stdin;
\.


--
-- TOC entry 4869 (class 0 OID 16560)
-- Dependencies: 216
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project (project_id, name, creation_time, status) FROM stdin;
1	Project One	2024-11-18 07:01:20	active
2	Project Two	2024-11-18 08:01:20	active
\.


--
-- TOC entry 4871 (class 0 OID 16598)
-- Dependencies: 218
-- Data for Name: skill; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.skill (skill_id, name, field) FROM stdin;
1	Front End Development Skills	Web Development
2	Backend Development Skills	Web Development
\.


--
-- TOC entry 4870 (class 0 OID 16581)
-- Dependencies: 217
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (task_id, description, deadline, project_id, freelancer_id) FROM stdin;
1	design button	\N	1	1
2	add button	\N	1	2
\.


--
-- TOC entry 4872 (class 0 OID 16605)
-- Dependencies: 219
-- Data for Name: task_skill; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_skill (task_skill_id, task_id, skill_id, required_level) FROM stdin;
1	1	1	intermediate
2	2	2	intermediate
\.


--
-- TOC entry 4708 (class 2606 OID 16580)
-- Name: freelancer freelancer_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freelancer
    ADD CONSTRAINT freelancer_pk PRIMARY KEY (freelancer_id);


--
-- TOC entry 4718 (class 2606 OID 16628)
-- Name: freelancer_skill freelancer_skill_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freelancer_skill
    ADD CONSTRAINT freelancer_skill_pk PRIMARY KEY (freelancer_skill_id);


--
-- TOC entry 4710 (class 2606 OID 16566)
-- Name: project project_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pk PRIMARY KEY (project_id);


--
-- TOC entry 4714 (class 2606 OID 16604)
-- Name: skill skill_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT skill_pk PRIMARY KEY (skill_id);


--
-- TOC entry 4712 (class 2606 OID 16587)
-- Name: task task_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pk PRIMARY KEY (task_id);


--
-- TOC entry 4716 (class 2606 OID 16611)
-- Name: task_skill task_skill_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_skill
    ADD CONSTRAINT task_skill_pk PRIMARY KEY (task_skill_id);


--
-- TOC entry 4719 (class 2606 OID 16593)
-- Name: task freelancer_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT freelancer_fk FOREIGN KEY (freelancer_id) REFERENCES public.freelancer(freelancer_id);


--
-- TOC entry 4723 (class 2606 OID 16629)
-- Name: freelancer_skill freelancer_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freelancer_skill
    ADD CONSTRAINT freelancer_fk FOREIGN KEY (freelancer_id) REFERENCES public.freelancer(freelancer_id);


--
-- TOC entry 4720 (class 2606 OID 16588)
-- Name: task project_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT project_fk FOREIGN KEY (project_id) REFERENCES public.project(project_id);


--
-- TOC entry 4724 (class 2606 OID 16634)
-- Name: freelancer_skill skill_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freelancer_skill
    ADD CONSTRAINT skill_fk FOREIGN KEY (skill_id) REFERENCES public.skill(skill_id);


--
-- TOC entry 4721 (class 2606 OID 16617)
-- Name: task_skill skill_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_skill
    ADD CONSTRAINT skill_id FOREIGN KEY (skill_id) REFERENCES public.skill(skill_id);


--
-- TOC entry 4722 (class 2606 OID 16612)
-- Name: task_skill task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_skill
    ADD CONSTRAINT task_id FOREIGN KEY (task_id) REFERENCES public.task(task_id);


-- Completed on 2024-11-18 07:24:55

--
-- PostgreSQL database dump complete
--

