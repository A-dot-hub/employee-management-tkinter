-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: employee_management
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employee_salary`
--

DROP TABLE IF EXISTS `employee_salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_salary` (
  `emp_id` varchar(10) NOT NULL,
  `emp_name` varchar(100) DEFAULT NULL,
  `base_pay` decimal(10,2) DEFAULT NULL,
  `present_days` int DEFAULT NULL,
  `medical` decimal(10,2) DEFAULT NULL,
  `conveyance` decimal(10,2) DEFAULT NULL,
  `pf` decimal(10,2) DEFAULT NULL,
  `net_salary` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_salary`
--

LOCK TABLES `employee_salary` WRITE;
/*!40000 ALTER TABLE `employee_salary` DISABLE KEYS */;
INSERT INTO `employee_salary` VALUES ('EN12314','jayesh',3000.00,20,2.00,23.00,2000.00,300000.00),('EN25978','Abhishek',20000.00,28,2.00,23.00,2333.00,20000.00),('EN73425','kiran',4000.00,30,2300.00,2344.00,1223.00,400000.00);
/*!40000 ALTER TABLE `employee_salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` varchar(255) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `age` int NOT NULL,
  `doj` date NOT NULL,
  `email` varchar(100) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `gender` enum('Male','Female') NOT NULL,
  `contact` varchar(15) NOT NULL,
  `address` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `contact` (`contact`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'EN25978','Abhishek',20,'2004-05-07','abhishek@gmail.com','computer','Male','9321675524','bandra east mumbai 400051\n'),(2,'EN12314','jayesh',24,'2008-09-06','jayesh@gmail.com','computer','Male','98765445254','kurla@gmail.com\n'),(3,'EN73425','kiran',23,'2006-06-01','kiran@gmail.com','computer','Male','646469899','Andheri east\n'),(4,'EN26848','lokesh',18,'2004-03-12','lokesk@gmail.com','computer','Male','9878967567','ghatkopar west\n'),(8,'EN22408','prince',12,'2004-12-02','pr@gmail.com','information technology','Male','2311546464','bandra east mumbai\n');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` varchar(10) NOT NULL,
  `pdf_file` longblob NOT NULL,
  `report_type` varchar(100) NOT NULL,
  `created_date` date NOT NULL,
  `created_by` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (1,'EN25978',_binary '%PDF-1.4\n%“Œ‹ž ReportLab Generated PDF document http://www.reportlab.com\n1 0 obj\n<<\n/F1 2 0 R /F2 3 0 R\n>>\nendobj\n2 0 obj\n<<\n/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font\n>>\nendobj\n3 0 obj\n<<\n/BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding /Name /F2 /Subtype /Type1 /Type /Font\n>>\nendobj\n4 0 obj\n<<\n/Contents 8 0 R /MediaBox [ 0 0 612 792 ] /Parent 7 0 R /Resources <<\n/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]\n>> /Rotate 0 /Trans <<\n\n>> \n  /Type /Page\n>>\nendobj\n5 0 obj\n<<\n/PageMode /UseNone /Pages 7 0 R /Type /Catalog\n>>\nendobj\n6 0 obj\n<<\n/Author (\\(anonymous\\)) /CreationDate (D:20250331164924+05\'00\') /Creator (\\(unspecified\\)) /Keywords () /ModDate (D:20250331164924+05\'00\') /Producer (ReportLab PDF Library - www.reportlab.com) \n  /Subject (\\(unspecified\\)) /Title (\\(anonymous\\)) /Trapped /False\n>>\nendobj\n7 0 obj\n<<\n/Count 1 /Kids [ 4 0 R ] /Type /Pages\n>>\nendobj\n8 0 obj\n<<\n/Filter [ /ASCII85Decode /FlateDecode ] /Length 695\n>>\nstream\nGas1]9lJc?%)(h*n<arp7`gfEjgGn,JRKMKf([$Qe0\\mGB241)s*g1a43CW5fV1o#qG@sK!U8S1G?t>uc/J7Q%U;9u$=#=mq%&kTUH]tE4>R)n$?@I6[^tU<6ngem,\"tR*\"E<Cr#iT94<6Psj+^`%[rpO`3Qgj(EFgHi+IMU1U#m,hW\"Siu,4%N*H`8HcL;\\n)7_u`\"96S9C;1h3!?^uDh=<qTqMr\\m-*+GYA.m\"@B>M.\'Jr8GNi60lXrRQgo)\"o;.qkYH#)2:KM$6?^_?SRWC%s.79psl*M\\QFCo(+JJjlLZG8#3X1>-0q)Trq[:7-B+u3gO]\\\\X8eOUf\"<hi)QNWDH]m3*b3J:t<lK_?HT=]:(&d:c)*ZPcQ^mA<\',2h@tW?$%\'KZd\"l]/ci-1^8r+%+e155]u2JeolYf+%.d&6JELB?1kuC]MOf+I(5E//(](eMB-A#M)5oIOQe?De>IsPJC]uSH.elbg#t5;BK-tC\\e)\"(Iaopt[AiIB)cRSKTA;HAO^I6uD?&-(a*bb/K^EmGuFHSTPgoBnC`=jO=]a\"AA!-HA9RcI4\\\\M(2mFOK*nBhsHTQ66YaOU5AMD[Kr-4^RiF;Z\'-?WRQZW;-egEY;[dJ#8<(4ZqSnUlpf0NX\'ATih#_0n\\?F(m;\'#LQ(Mn3rFVUcJRS]Jo4csn3A2F@_OC9u]kWcrC5VN~>endstream\nendobj\nxref\n0 9\n0000000000 65535 f \n0000000073 00000 n \n0000000114 00000 n \n0000000221 00000 n \n0000000333 00000 n \n0000000526 00000 n \n0000000594 00000 n \n0000000877 00000 n \n0000000936 00000 n \ntrailer\n<<\n/ID \n[<759d4fefe38ffce3ed848fdc8a14a118><759d4fefe38ffce3ed848fdc8a14a118>]\n% ReportLab generated PDF document -- digest (http://www.reportlab.com)\n\n/Info 6 0 R\n/Root 5 0 R\n/Size 9\n>>\nstartxref\n1721\n%%EOF\n','custom','2025-03-31','Abhishek');
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salary_slips`
--

DROP TABLE IF EXISTS `salary_slips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salary_slips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` varchar(10) NOT NULL,
  `pdf_file` longblob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary_slips`
--

LOCK TABLES `salary_slips` WRITE;
/*!40000 ALTER TABLE `salary_slips` DISABLE KEYS */;
INSERT INTO `salary_slips` VALUES (1,'EN25978',_binary '%PDF-1.3\n%“Œ‹ž ReportLab Generated PDF document http://www.reportlab.com\n1 0 obj\n<<\n/F1 2 0 R /F2 3 0 R\n>>\nendobj\n2 0 obj\n<<\n/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font\n>>\nendobj\n3 0 obj\n<<\n/BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding /Name /F2 /Subtype /Type1 /Type /Font\n>>\nendobj\n4 0 obj\n<<\n/Contents 8 0 R /MediaBox [ 0 0 612 792 ] /Parent 7 0 R /Resources <<\n/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]\n>> /Rotate 0 /Trans <<\n\n>> \n  /Type /Page\n>>\nendobj\n5 0 obj\n<<\n/PageMode /UseNone /Pages 7 0 R /Type /Catalog\n>>\nendobj\n6 0 obj\n<<\n/Author (anonymous) /CreationDate (D:20250330184220+05\'00\') /Creator (ReportLab PDF Library - www.reportlab.com) /Keywords () /ModDate (D:20250330184220+05\'00\') /Producer (ReportLab PDF Library - www.reportlab.com) \n  /Subject (unspecified) /Title (untitled) /Trapped /False\n>>\nendobj\n7 0 obj\n<<\n/Count 1 /Kids [ 4 0 R ] /Type /Pages\n>>\nendobj\n8 0 obj\n<<\n/Filter [ /ASCII85Decode /FlateDecode ] /Length 355\n>>\nstream\nGasbVd8#<J(kqGQ\'^&AR@`s9FG>;7LU1A7lJI9.2$3aWfiU(2\\VfOS+g@XAMh`60^bJAqPG@sqWF+NW\\#Bq=t^cf_jGX*H\"45CpASK9cL\\\'D+0b8=hTK;`aT<)$Ni6s.Q/l5m\"3B[.c-+YLLaISVu6nZ<`lEP%8V,cU+ebefuia&EVA:oUNE_X6rl0H5<W!J<NpQ\\M`/I=s!.Cp1gF_q57XmCB&?6`NR+HP=49)q!ITO-CHK/8`aYM!a3)<ZfgaQ\'%o?UR5uC==t.`hIUP$Wrk?[\"1<9IeCnR5D]uic<=FjsfFh=m2-ilOC/\'SmCak,W^;M<s%9\'?nCcbA<o\\L=OEp(L^P>BR9V9&~>endstream\nendobj\nxref\n0 9\n0000000000 65535 f \n0000000073 00000 n \n0000000114 00000 n \n0000000221 00000 n \n0000000333 00000 n \n0000000526 00000 n \n0000000594 00000 n \n0000000890 00000 n \n0000000949 00000 n \ntrailer\n<<\n/ID \n[<19bc751d749ef5685a3cabcd34c97faf><19bc751d749ef5685a3cabcd34c97faf>]\n% ReportLab generated PDF document -- digest (http://www.reportlab.com)\n\n/Info 6 0 R\n/Root 5 0 R\n/Size 9\n>>\nstartxref\n1394\n%%EOF\n'),(3,'EN73425',_binary '%PDF-1.3\n%“Œ‹ž ReportLab Generated PDF document http://www.reportlab.com\n1 0 obj\n<<\n/F1 2 0 R /F2 3 0 R /F3 4 0 R\n>>\nendobj\n2 0 obj\n<<\n/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font\n>>\nendobj\n3 0 obj\n<<\n/BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding /Name /F2 /Subtype /Type1 /Type /Font\n>>\nendobj\n4 0 obj\n<<\n/BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding /Name /F3 /Subtype /Type1 /Type /Font\n>>\nendobj\n5 0 obj\n<<\n/Contents 9 0 R /MediaBox [ 0 0 612 792 ] /Parent 8 0 R /Resources <<\n/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]\n>> /Rotate 0 /Trans <<\n\n>> \n  /Type /Page\n>>\nendobj\n6 0 obj\n<<\n/PageMode /UseNone /Pages 8 0 R /Type /Catalog\n>>\nendobj\n7 0 obj\n<<\n/Author (anonymous) /CreationDate (D:20250331195334+05\'00\') /Creator (ReportLab PDF Library - www.reportlab.com) /Keywords () /ModDate (D:20250331195334+05\'00\') /Producer (ReportLab PDF Library - www.reportlab.com) \n  /Subject (unspecified) /Title (untitled) /Trapped /False\n>>\nendobj\n8 0 obj\n<<\n/Count 1 /Kids [ 5 0 R ] /Type /Pages\n>>\nendobj\n9 0 obj\n<<\n/Filter [ /ASCII85Decode /FlateDecode ] /Length 564\n>>\nstream\nGasId?#SFN\'Rf.GS@rdi88T^Tb$-=%Wl/QROet]sET+biLs>:^;uV39%qoAt;f3T>`ol-(O,l;gH[)qN;d^=\"qOW<I`,\"kX$P6)gM*\"^DJG6)AN@3TR]V47,6f5RsMU.K.^XE>um^1Y_,I9cg6nas`Bt!TH+T@AqlH&:DZ\\nJiWuiBboj9J2g>KS$gU/q4_BMip\'o[i2L!SXRZ\\i2jd.%==_e_@@,p-Xb_r*<f_W\\#Ql@\'hp%\'\"Js%eEI`_P-h=*cl<_]q,2=@epq4ch+Jsa/N>:?N3^\"a70_)=l0`XGfk2]3`gPQ;]9,7(o^\\8IZ57;98I+5`8#YE(h4Us/[/j4aH.^5@4VdJFL#1AKJtdJ)m,:\"gspP;AF4NV7Z\':0?DrtR5S(XQBEpG17/%PI.USK*X.`c(^E)$!18>6c\\Wc0H.0\"(lOl_-.3H*@R:Tg_D]?K^NG(+`ZptH0R7r>f3[2aD4?ZO3%UtVQi3Ln@a9Vq\"JdU^^?khI:*R=;`oidbGK2Cs]=$OL%iN7..VfWs<Zql`g72VBLHjmFH4qNE:]:+dqUY<b#H_>~>endstream\nendobj\nxref\n0 10\n0000000000 65535 f \n0000000073 00000 n \n0000000124 00000 n \n0000000231 00000 n \n0000000343 00000 n \n0000000458 00000 n \n0000000651 00000 n \n0000000719 00000 n \n0000001015 00000 n \n0000001074 00000 n \ntrailer\n<<\n/ID \n[<bf6dff214e140636c86f67f96ec07dd1><bf6dff214e140636c86f67f96ec07dd1>]\n% ReportLab generated PDF document -- digest (http://www.reportlab.com)\n\n/Info 7 0 R\n/Root 6 0 R\n/Size 10\n>>\nstartxref\n1728\n%%EOF\n'),(4,'EN12314',_binary '%PDF-1.3\n%“Œ‹ž ReportLab Generated PDF document http://www.reportlab.com\n1 0 obj\n<<\n/F1 2 0 R /F2 3 0 R /F3 4 0 R\n>>\nendobj\n2 0 obj\n<<\n/BaseFont /Helvetica /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font\n>>\nendobj\n3 0 obj\n<<\n/BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding /Name /F2 /Subtype /Type1 /Type /Font\n>>\nendobj\n4 0 obj\n<<\n/BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding /Name /F3 /Subtype /Type1 /Type /Font\n>>\nendobj\n5 0 obj\n<<\n/Contents 9 0 R /MediaBox [ 0 0 612 792 ] /Parent 8 0 R /Resources <<\n/Font 1 0 R /ProcSet [ /PDF /Text /ImageB /ImageC /ImageI ]\n>> /Rotate 0 /Trans <<\n\n>> \n  /Type /Page\n>>\nendobj\n6 0 obj\n<<\n/PageMode /UseNone /Pages 8 0 R /Type /Catalog\n>>\nendobj\n7 0 obj\n<<\n/Author (anonymous) /CreationDate (D:20250331194551+05\'00\') /Creator (ReportLab PDF Library - www.reportlab.com) /Keywords () /ModDate (D:20250331194551+05\'00\') /Producer (ReportLab PDF Library - www.reportlab.com) \n  /Subject (unspecified) /Title (untitled) /Trapped /False\n>>\nendobj\n8 0 obj\n<<\n/Count 1 /Kids [ 5 0 R ] /Type /Pages\n>>\nendobj\n9 0 obj\n<<\n/Filter [ /ASCII85Decode /FlateDecode ] /Length 557\n>>\nstream\nGasIdd;IYl\'Rf-pcJH-IUiq?@nl?+\".PV])UhN_6>e&.f`+F2@.=Y\\PEEQ]PPT*,5EmDA]jHtS1Mq@8=\",7,bmPoHIA-Lfr3_1S7-`q\\Z\"Rjq=f0T1UT6gnt(jbUF10fdEm7*F1\\CG2lNQb>\'&AR<--M]FlMW=r_jc28$B/T-4ejt1ml9AfW[Dl!Z?<>i3#kM$+2.TBCL(XGRc\"`!dI4ONV.C3n@<.\'Y8#=HF;#fB=8WI+ReZVuq6FdRX_$6?.e)k$;eaj\'/gk*(Sq:t,G-go5>M]=e<M*_$6jVqe98m\'H)Q%NV.`N!=Nh-/%GpYc**^V\'X\'c*+3@\\B)lEB@jbYjBPbbQat]\'U*B:Bd,K+_WpeK\"S+ZE,fn733kNO[O(NCrGaVaj1R@GZk9%O5-mM^i3XGYXRoDG2M\">]-A5jMs9ZGN>>0\\QmSr5?ufr[oq2j=X_R-3tQ)*M;\'X`Nk=;S\\<CR)?;]th0&h,M.e$YVEp+6[@??\\s^)S#qcd3K\"-+.\\<@8!(gem@f7[[VC9%8+O8CF/ShSH;0nMq$,1iC)uPrM]fB~>endstream\nendobj\nxref\n0 10\n0000000000 65535 f \n0000000073 00000 n \n0000000124 00000 n \n0000000231 00000 n \n0000000343 00000 n \n0000000458 00000 n \n0000000651 00000 n \n0000000719 00000 n \n0000001015 00000 n \n0000001074 00000 n \ntrailer\n<<\n/ID \n[<b2a9ed5f99d962eb4cf8e78286c9c7fa><b2a9ed5f99d962eb4cf8e78286c9c7fa>]\n% ReportLab generated PDF document -- digest (http://www.reportlab.com)\n\n/Info 7 0 R\n/Root 6 0 R\n/Size 10\n>>\nstartxref\n1721\n%%EOF\n');
/*!40000 ALTER TABLE `salary_slips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'abhishek','9321675524'),(2,'kiran','753489621'),(3,'prince@123','93216p2');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-19  8:55:52
