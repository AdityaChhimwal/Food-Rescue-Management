**Project Overview:**  

Food waste represents a critical environmental and social challenge, with restaurants, bakeries, and grocery stores
discarding approximately 40% of food produced while communities face food insecurity. Local businesses lack
efficient coordination mechanisms to connect surplus food with those who need it before spoilage occurs.
Primary Goal: Develop a comprehensive MySQL database-driven platform enabling efficient food rescue through
tiered access - free priority for verified charities and low-cost access for community members.
 Technical Objectives:
- Design normalized relational database supporting time-sensitive food listings, geospatial matching, user role
management, and transaction integrity
- Implement complex database operations, including concurrent claiming processes, time-based data cleanup,
and analytics reporting
- Create scalable system architecture supporting multiple user types with distinct access privileges.

**#Updated Updated Project Approach and Architecture**
Our approach centers on database-first design, leveraging MySQL's robust capabilities for complex relational
operations and time-sensitive data management. We prioritize DBMS concepts demonstration through practical
implementation of advanced database features.
Database Architecture: MySQL serves as the foundation, featuring normalized tables with complex relationships,
foreign key constraints, and advanced indexing strategies. Implementation includes geospatial distance
calculations, time-based automated cleanup, and role-based access control, demonstrating sophisticated database
design principles.
Backend Development: Python with Flask framework provides RESTful API services managing authentication,
business logic, and data persistence. The backend handles complex claiming transactions ensuring data integrity,
implements charity priority algorithms, and manages user role hierarchies with appropriate access controls.
Frontend Implementation: HTML/CSS/JavaScript with Tailwind CSS creates intuitive, responsive interfaces
supporting distinct user workflows for businesses, charities, and community members. The interface prioritizes
rapid food claiming processes and clear pickup coordination while maintaining scalability for future payment
integration
