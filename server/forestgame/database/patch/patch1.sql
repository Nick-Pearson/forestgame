ALTER TABLE `client` RENAME COLUMN user_agent_type TO user_os_version;
ALTER TABLE `client` RENAME COLUMN user_agent_family TO user_browser_name;
ALTER TABLE `client` RENAME COLUMN user_agent_name TO user_browser_version;
ALTER TABLE client ADD bot BOOLEAN NULL;