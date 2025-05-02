--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-02 23:23:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 228 (class 1259 OID 16681)
-- Name: belirti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.belirti (
    id integer NOT NULL,
    hasta_id integer,
    tarih date NOT NULL,
    belirti_turu character varying(30)
);


ALTER TABLE public.belirti OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16680)
-- Name: belirti_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.belirti_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.belirti_id_seq OWNER TO postgres;

--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 227
-- Name: belirti_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.belirti_id_seq OWNED BY public.belirti.id;


--
-- TOC entry 226 (class 1259 OID 16669)
-- Name: diyet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diyet (
    id integer NOT NULL,
    hasta_id integer,
    tarih date NOT NULL,
    diyet_turu character varying(30),
    diyet_uygulandi boolean
);


ALTER TABLE public.diyet OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16668)
-- Name: diyet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diyet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diyet_id_seq OWNER TO postgres;

--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 225
-- Name: diyet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diyet_id_seq OWNED BY public.diyet.id;


--
-- TOC entry 224 (class 1259 OID 16657)
-- Name: egzersiz; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.egzersiz (
    id integer NOT NULL,
    hasta_id integer,
    tarih date NOT NULL,
    egzersiz_turu character varying(30),
    egzersiz_durumu boolean
);


ALTER TABLE public.egzersiz OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16656)
-- Name: egzersiz_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.egzersiz_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.egzersiz_id_seq OWNER TO postgres;

--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 223
-- Name: egzersiz_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.egzersiz_id_seq OWNED BY public.egzersiz.id;


--
-- TOC entry 220 (class 1259 OID 16623)
-- Name: hasta_doktor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hasta_doktor (
    id integer NOT NULL,
    hasta_id integer,
    doktor_id integer
);


ALTER TABLE public.hasta_doktor OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16622)
-- Name: hasta_doktor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hasta_doktor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hasta_doktor_id_seq OWNER TO postgres;

--
-- TOC entry 4983 (class 0 OID 0)
-- Dependencies: 219
-- Name: hasta_doktor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hasta_doktor_id_seq OWNED BY public.hasta_doktor.id;


--
-- TOC entry 232 (class 1259 OID 16707)
-- Name: insulin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insulin (
    id integer NOT NULL,
    hasta_id integer,
    tarih date NOT NULL,
    ortalama_seker double precision,
    doz_miktari double precision
);


ALTER TABLE public.insulin OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16706)
-- Name: insulin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.insulin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.insulin_id_seq OWNER TO postgres;

--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 231
-- Name: insulin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.insulin_id_seq OWNED BY public.insulin.id;


--
-- TOC entry 218 (class 1259 OID 16610)
-- Name: kullanici; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kullanici (
    id integer NOT NULL,
    tc_kimlik_no character varying(11) NOT NULL,
    ad character varying(50) NOT NULL,
    soyad character varying(50) NOT NULL,
    dogum_tarihi date,
    sifre_hash text NOT NULL,
    cinsiyet character varying(10),
    rol character varying(10) NOT NULL,
    eposta character varying(100),
    profil_resmi bytea
);


ALTER TABLE public.kullanici OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16609)
-- Name: kullanici_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kullanici_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kullanici_id_seq OWNER TO postgres;

--
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 217
-- Name: kullanici_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kullanici_id_seq OWNED BY public.kullanici.id;


--
-- TOC entry 222 (class 1259 OID 16640)
-- Name: olcum; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olcum (
    id integer NOT NULL,
    hasta_id integer,
    doktor_id integer,
    tarih_saat timestamp without time zone NOT NULL,
    kan_seker_degeri integer NOT NULL,
    olcum_zamani character varying(15),
    ortalamaya_dahil boolean
);


ALTER TABLE public.olcum OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16639)
-- Name: olcum_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.olcum_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.olcum_id_seq OWNER TO postgres;

--
-- TOC entry 4986 (class 0 OID 0)
-- Dependencies: 221
-- Name: olcum_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.olcum_id_seq OWNED BY public.olcum.id;


--
-- TOC entry 230 (class 1259 OID 16693)
-- Name: uyari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.uyari (
    id integer NOT NULL,
    hasta_id integer,
    tarih_saat timestamp without time zone NOT NULL,
    uyari_turu character varying(50),
    mesaj text
);


ALTER TABLE public.uyari OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16692)
-- Name: uyari_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.uyari_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.uyari_id_seq OWNER TO postgres;

--
-- TOC entry 4987 (class 0 OID 0)
-- Dependencies: 229
-- Name: uyari_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.uyari_id_seq OWNED BY public.uyari.id;


--
-- TOC entry 4782 (class 2604 OID 16684)
-- Name: belirti id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirti ALTER COLUMN id SET DEFAULT nextval('public.belirti_id_seq'::regclass);


--
-- TOC entry 4781 (class 2604 OID 16672)
-- Name: diyet id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyet ALTER COLUMN id SET DEFAULT nextval('public.diyet_id_seq'::regclass);


--
-- TOC entry 4780 (class 2604 OID 16660)
-- Name: egzersiz id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz ALTER COLUMN id SET DEFAULT nextval('public.egzersiz_id_seq'::regclass);


--
-- TOC entry 4778 (class 2604 OID 16626)
-- Name: hasta_doktor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasta_doktor ALTER COLUMN id SET DEFAULT nextval('public.hasta_doktor_id_seq'::regclass);


--
-- TOC entry 4784 (class 2604 OID 16710)
-- Name: insulin id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insulin ALTER COLUMN id SET DEFAULT nextval('public.insulin_id_seq'::regclass);


--
-- TOC entry 4777 (class 2604 OID 16613)
-- Name: kullanici id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kullanici ALTER COLUMN id SET DEFAULT nextval('public.kullanici_id_seq'::regclass);


--
-- TOC entry 4779 (class 2604 OID 16643)
-- Name: olcum id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olcum ALTER COLUMN id SET DEFAULT nextval('public.olcum_id_seq'::regclass);


--
-- TOC entry 4783 (class 2604 OID 16696)
-- Name: uyari id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyari ALTER COLUMN id SET DEFAULT nextval('public.uyari_id_seq'::regclass);


--
-- TOC entry 4970 (class 0 OID 16681)
-- Dependencies: 228
-- Data for Name: belirti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.belirti (id, hasta_id, tarih, belirti_turu) FROM stdin;
\.


--
-- TOC entry 4968 (class 0 OID 16669)
-- Dependencies: 226
-- Data for Name: diyet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.diyet (id, hasta_id, tarih, diyet_turu, diyet_uygulandi) FROM stdin;
\.


--
-- TOC entry 4966 (class 0 OID 16657)
-- Dependencies: 224
-- Data for Name: egzersiz; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.egzersiz (id, hasta_id, tarih, egzersiz_turu, egzersiz_durumu) FROM stdin;
\.


--
-- TOC entry 4962 (class 0 OID 16623)
-- Dependencies: 220
-- Data for Name: hasta_doktor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hasta_doktor (id, hasta_id, doktor_id) FROM stdin;
1	2	1
\.


--
-- TOC entry 4974 (class 0 OID 16707)
-- Dependencies: 232
-- Data for Name: insulin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insulin (id, hasta_id, tarih, ortalama_seker, doz_miktari) FROM stdin;
1	2	2025-05-02	145	1
2	2	2025-05-02	145	1
\.


--
-- TOC entry 4960 (class 0 OID 16610)
-- Dependencies: 218
-- Data for Name: kullanici; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kullanici (id, tc_kimlik_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, rol, eposta, profil_resmi) FROM stdin;
1	11111111111	Dr. Ayşe	Yılmaz	1980-01-01	hashlenmis1234	Kadın	doktor	ayse.doktor@example.com	\N
2	22222222222	Ali	Kaya	2002-05-10	1234	Erkek	hasta	ali.hasta@example.com	\N
\.


--
-- TOC entry 4964 (class 0 OID 16640)
-- Dependencies: 222
-- Data for Name: olcum; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.olcum (id, hasta_id, doktor_id, tarih_saat, kan_seker_degeri, olcum_zamani, ortalamaya_dahil) FROM stdin;
1	2	1	2025-05-02 22:31:57.224429	145	ogle	t
\.


--
-- TOC entry 4972 (class 0 OID 16693)
-- Dependencies: 230
-- Data for Name: uyari; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.uyari (id, hasta_id, tarih_saat, uyari_turu, mesaj) FROM stdin;
\.


--
-- TOC entry 4988 (class 0 OID 0)
-- Dependencies: 227
-- Name: belirti_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.belirti_id_seq', 1, false);


--
-- TOC entry 4989 (class 0 OID 0)
-- Dependencies: 225
-- Name: diyet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.diyet_id_seq', 1, false);


--
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 223
-- Name: egzersiz_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.egzersiz_id_seq', 1, false);


--
-- TOC entry 4991 (class 0 OID 0)
-- Dependencies: 219
-- Name: hasta_doktor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hasta_doktor_id_seq', 1, true);


--
-- TOC entry 4992 (class 0 OID 0)
-- Dependencies: 231
-- Name: insulin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.insulin_id_seq', 2, true);


--
-- TOC entry 4993 (class 0 OID 0)
-- Dependencies: 217
-- Name: kullanici_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kullanici_id_seq', 2, true);


--
-- TOC entry 4994 (class 0 OID 0)
-- Dependencies: 221
-- Name: olcum_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.olcum_id_seq', 1, true);


--
-- TOC entry 4995 (class 0 OID 0)
-- Dependencies: 229
-- Name: uyari_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.uyari_id_seq', 1, false);


--
-- TOC entry 4800 (class 2606 OID 16686)
-- Name: belirti belirti_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirti
    ADD CONSTRAINT belirti_pkey PRIMARY KEY (id);


--
-- TOC entry 4798 (class 2606 OID 16674)
-- Name: diyet diyet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyet
    ADD CONSTRAINT diyet_pkey PRIMARY KEY (id);


--
-- TOC entry 4796 (class 2606 OID 16662)
-- Name: egzersiz egzersiz_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz
    ADD CONSTRAINT egzersiz_pkey PRIMARY KEY (id);


--
-- TOC entry 4792 (class 2606 OID 16628)
-- Name: hasta_doktor hasta_doktor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasta_doktor
    ADD CONSTRAINT hasta_doktor_pkey PRIMARY KEY (id);


--
-- TOC entry 4804 (class 2606 OID 16712)
-- Name: insulin insulin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insulin
    ADD CONSTRAINT insulin_pkey PRIMARY KEY (id);


--
-- TOC entry 4786 (class 2606 OID 16621)
-- Name: kullanici kullanici_eposta_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kullanici
    ADD CONSTRAINT kullanici_eposta_key UNIQUE (eposta);


--
-- TOC entry 4788 (class 2606 OID 16617)
-- Name: kullanici kullanici_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kullanici
    ADD CONSTRAINT kullanici_pkey PRIMARY KEY (id);


--
-- TOC entry 4790 (class 2606 OID 16619)
-- Name: kullanici kullanici_tc_kimlik_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kullanici
    ADD CONSTRAINT kullanici_tc_kimlik_no_key UNIQUE (tc_kimlik_no);


--
-- TOC entry 4794 (class 2606 OID 16645)
-- Name: olcum olcum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olcum
    ADD CONSTRAINT olcum_pkey PRIMARY KEY (id);


--
-- TOC entry 4802 (class 2606 OID 16700)
-- Name: uyari uyari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyari
    ADD CONSTRAINT uyari_pkey PRIMARY KEY (id);


--
-- TOC entry 4811 (class 2606 OID 16687)
-- Name: belirti belirti_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirti
    ADD CONSTRAINT belirti_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4810 (class 2606 OID 16675)
-- Name: diyet diyet_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyet
    ADD CONSTRAINT diyet_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4809 (class 2606 OID 16663)
-- Name: egzersiz egzersiz_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz
    ADD CONSTRAINT egzersiz_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4805 (class 2606 OID 16634)
-- Name: hasta_doktor hasta_doktor_doktor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasta_doktor
    ADD CONSTRAINT hasta_doktor_doktor_id_fkey FOREIGN KEY (doktor_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4806 (class 2606 OID 16629)
-- Name: hasta_doktor hasta_doktor_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hasta_doktor
    ADD CONSTRAINT hasta_doktor_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4813 (class 2606 OID 16713)
-- Name: insulin insulin_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insulin
    ADD CONSTRAINT insulin_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4807 (class 2606 OID 16651)
-- Name: olcum olcum_doktor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olcum
    ADD CONSTRAINT olcum_doktor_id_fkey FOREIGN KEY (doktor_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4808 (class 2606 OID 16646)
-- Name: olcum olcum_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olcum
    ADD CONSTRAINT olcum_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


--
-- TOC entry 4812 (class 2606 OID 16701)
-- Name: uyari uyari_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyari
    ADD CONSTRAINT uyari_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.kullanici(id) ON DELETE CASCADE;


-- Completed on 2025-05-02 23:23:56

--
-- PostgreSQL database dump complete
--

