-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb:3306
-- Erstellungszeit: 26. Feb 2025 um 13:32
-- Server-Version: 10.2.44-MariaDB-1:10.2.44+maria~bionic
-- PHP-Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `backend`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `gruppe`
--

CREATE TABLE `gruppe` (
  `Gruppen_id` int(11) NOT NULL,
  `Gruppenname` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Daten für Tabelle `gruppe`
--

INSERT INTO `gruppe` (`Gruppen_id`, `Gruppenname`) VALUES
(1, 'Frontend'),
(2, 'Backend'),
(3, 'Infrastruktur');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `prio`
--

CREATE TABLE `prio` (
  `Prio_id` int(11) NOT NULL,
  `anzeigename` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `sprint`
--

CREATE TABLE `sprint` (
  `Sprint_id` int(11) NOT NULL,
  `Datum_Beginn` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `Datum_Ende` varchar(10) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Daten für Tabelle `sprint`
--

INSERT INTO `sprint` (`Sprint_id`, `Datum_Beginn`, `Datum_Ende`) VALUES
(104, '06.01.2025', '12.01.2025'),
(105, '13.01.2025', '19.01.2025'),
(106, '20.01.2025', '26.01.2025'),
(107, '27.01.2025', '02.02.2025'),
(108, '03.02.2025', '09.02.2025'),
(109, '10.02.2025', '16.02.2025'),
(110, '17.02.2025', '23.02.2025'),
(111, '24.02.2025', '02.03.2025'),
(112, '03.03.2025', '09.03.2025'),
(113, '10.03.2025', '16.03.2025'),
(114, '17.03.2025', '23.03.2025'),
(115, '24.03.2025', '30.03.2025'),
(116, '31.03.2025', '06.04.2025'),
(117, '07.04.2025', '13.04.2025'),
(118, '14.04.2025', '20.04.2025'),
(119, '21.04.2025', '27.04.2025'),
(120, '28.04.2025', '04.05.2025'),
(121, '05.05.2025', '11.05.2025'),
(122, '12.05.2025', '18.05.2025'),
(123, '19.05.2025', '25.05.2025'),
(124, '26.05.2025', '01.06.2025'),
(125, '02.06.2025', '08.06.2025'),
(126, '09.06.2025', '15.06.2025'),
(127, '16.06.2025', '22.06.2025'),
(128, '23.06.2025', '29.06.2025'),
(129, '30.06.2025', '06.07.2025'),
(130, '07.07.2025', '13.07.2025'),
(131, '14.07.2025', '20.07.2025'),
(132, '21.07.2025', '27.07.2025'),
(133, '28.07.2025', '03.08.2025'),
(134, '04.08.2025', '10.08.2025'),
(135, '11.08.2025', '17.08.2025'),
(136, '18.08.2025', '24.08.2025'),
(137, '25.08.2025', '31.08.2025'),
(138, '01.09.2025', '07.09.2025'),
(139, '08.09.2025', '14.09.2025'),
(140, '15.09.2025', '21.09.2025'),
(141, '22.09.2025', '28.09.2025'),
(142, '29.09.2025', '05.10.2025'),
(143, '06.10.2025', '12.10.2025'),
(144, '13.10.2025', '19.10.2025'),
(145, '20.10.2025', '26.10.2025'),
(146, '27.10.2025', '02.11.2025'),
(147, '03.11.2025', '09.11.2025'),
(148, '10.11.2025', '16.11.2025'),
(149, '17.11.2025', '23.11.2025'),
(150, '24.11.2025', '30.11.2025'),
(151, '01.12.2025', '07.12.2025'),
(152, '08.12.2025', '14.12.2025'),
(153, '15.12.2025', '21.12.2025'),
(154, '22.12.2025', '28.12.2025');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `status`
--

CREATE TABLE `status` (
  `status_id` int(11) NOT NULL,
  `anzeigename` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ticket_data`
--

CREATE TABLE `ticket_data` (
  `Ticket_id` int(11) NOT NULL,
  `Benutzer_id` int(11) NOT NULL,
  `Betreff` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `Beschreibung` text COLLATE utf8_unicode_ci NOT NULL,
  `Status` int(11) NOT NULL,
  `Prio` int(11) DEFAULT NULL,
  `Team` int(11) DEFAULT NULL,
  `Erstelldatum` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Sprint` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Daten für Tabelle `ticket_data`
--

INSERT INTO `ticket_data` (`Ticket_id`, `Benutzer_id`, `Betreff`, `Beschreibung`, `Status`, `Prio`, `Team`, `Erstelldatum`, `Sprint`) VALUES
(1, 0, 'Hilfe!', 'ich muss hier raus!', 5, 3, 3, '2025-02-25', 11),
(2, 0, 'Hilfe!', 'ich muss hier raus!', 0, NULL, NULL, '25.02.2025', NULL),
(3, 0, 'Hilde brauch Hilfe', 'Und das ist schlecht', 0, NULL, 1, '26.02.2025', NULL);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user_data`
--

CREATE TABLE `user_data` (
  `Benutzer_id` int(11) NOT NULL,
  `Benutzername` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Passwort` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Gruppe` int(11) DEFAULT NULL,
  `Rolle` int(11) NOT NULL DEFAULT 0,
  `Sperren` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Daten für Tabelle `user_data`
--

INSERT INTO `user_data` (`Benutzer_id`, `Benutzername`, `Email`, `Passwort`, `Gruppe`, `Rolle`, `Sperren`) VALUES
(1, 'asdasd', 'sadsad', 'sads', NULL, 0, 0);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `gruppe`
--
ALTER TABLE `gruppe`
  ADD PRIMARY KEY (`Gruppen_id`);

--
-- Indizes für die Tabelle `prio`
--
ALTER TABLE `prio`
  ADD PRIMARY KEY (`Prio_id`);

--
-- Indizes für die Tabelle `sprint`
--
ALTER TABLE `sprint`
  ADD PRIMARY KEY (`Sprint_id`);

--
-- Indizes für die Tabelle `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`status_id`);

--
-- Indizes für die Tabelle `ticket_data`
--
ALTER TABLE `ticket_data`
  ADD PRIMARY KEY (`Ticket_id`);

--
-- Indizes für die Tabelle `user_data`
--
ALTER TABLE `user_data`
  ADD PRIMARY KEY (`Benutzer_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `gruppe`
--
ALTER TABLE `gruppe`
  MODIFY `Gruppen_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT für Tabelle `prio`
--
ALTER TABLE `prio`
  MODIFY `Prio_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `sprint`
--
ALTER TABLE `sprint`
  MODIFY `Sprint_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=155;

--
-- AUTO_INCREMENT für Tabelle `status`
--
ALTER TABLE `status`
  MODIFY `status_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `ticket_data`
--
ALTER TABLE `ticket_data`
  MODIFY `Ticket_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT für Tabelle `user_data`
--
ALTER TABLE `user_data`
  MODIFY `Benutzer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
