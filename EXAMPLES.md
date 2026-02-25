# AutoDev-AI - Example Generated Projects

## Sample Prompts & Expected Output

### Example 1: Simple Task Manager

#### Input Prompt
```
Build a simple task manager application with user authentication, 
task creation, marking complete, and PostgreSQL database.
```

#### Generated Project Structure
```
generated_projects/{project-id}/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app setup
│   │   ├── models.py        # User, Task SQLAlchemy models
│   │   ├── routes.py        # /auth, /tasks endpoints
│   │   └── __init__.py
│   ├── requirements.txt      # fastapi, sqlalchemy, pydantic, etc.
│   └── Dockerfile           # Python 3.11 slim
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx       # Root layout with navigation
│   │   ├── page.tsx         # Dashboard with task list
│   │   └── globals.css
│   ├── components/
│   │   ├── TaskForm.tsx     # Add task form
│   │   └── TaskItem.tsx     # Individual task component
│   ├── services/
│   │   └── api.ts           # API client
│   └── package.json
│
├── docker-compose.yml       # Services: postgres, redis, backend, frontend
├── .env.example             # Environment variables
└── README.md                # Project documentation
```

#### Expected Features
- Login/register endpoints
- JWT token authentication
- Create/read/update/delete tasks
- Mark tasks as complete
- User-specific task filtering
- Responsive UI with Tailwind
- Database migrations support

---

### Example 2: Blog Platform

#### Input Prompt
```
Create a blog platform with user profiles, blog posts, comments, 
like system, and full-text search using Next.js and FastAPI.
```

#### Generated API Endpoints
```
POST   /api/auth/register          # User registration
POST   /api/auth/login             # User login
GET    /api/posts                  # List posts (paginated)
POST   /api/posts                  # Create post
GET    /api/posts/{id}             # Get post with comments
PUT    /api/posts/{id}             # Update post
DELETE /api/posts/{id}             # Delete post
POST   /api/posts/{id}/comments    # Add comment
POST   /api/posts/{id}/like        # Like post
GET    /api/search?q=...           # Full-text search
GET    /api/users/{id}             # User profile
GET    /api/users/{id}/posts       # User's posts
```

#### Expected Database Schema
```sql
users (id, username, email, password_hash, bio, avatar, created_at)
posts (id, user_id, title, content, created_at, updated_at)
comments (id, post_id, user_id, content, created_at)
likes (id, post_id, user_id, created_at)
```

#### Frontend Pages
```
/ (Home)                    # Blog feed
/post/{id}                  # Blog post detail
/create                     # Create post
/search                     # Search results
/profile/{username}         # User profile
/settings                   # User settings
/login                      # Authentication
/register                   # Registration
```

---

### Example 3: E-commerce Store

#### Input Prompt
```
Build an e-commerce platform with product catalog, shopping cart, 
checkout, payment integration, and order history using PostgreSQL, 
FastAPI, and React.
```

#### Generated Database Tables
```
users
├── id, email, password_hash, name, address, created_at

products
├── id, name, description, price, category, stock, image_url

categories
├── id, name, description

orders
├── id, user_id, total_price, status, created_at

order_items
├── id, order_id, product_id, quantity, price

shopping_carts
├── id, user_id, product_id, quantity, created_at

payments
├── id, order_id, amount, status, payment_method
```

#### Generated API Features
```
GET    /api/products                 # List with pagination
GET    /api/products/{id}            # Product details
POST   /api/cart                     # Add to cart
GET    /api/cart                     # View cart
DELETE /api/cart/{item_id}           # Remove from cart
POST   /api/orders                   # Create order
GET    /api/orders                   # Order history
GET    /api/orders/{id}              # Order details
POST   /api/payments                 # Process payment
GET    /api/categories               # List categories
```

#### Frontend Components
```
ProductGrid        # Display products in grid
ProductDetail      # Single product page
ShoppingCart       # Cart management
Checkout          # Order checkout
OrderHistory      # View previous orders
UserProfile       # Account management
Navigation        # Header with search
FilterSidebar     # Category & price filters
```

---

### Example 4: Real-time Chat Application

#### Input Prompt
```
Create a real-time chat application with private messages, group chats,
user presence, typing indicators, and message history using WebSockets,
FastAPI, and Next.js.
```

#### Generated Features
```
Users
├── Registration & login
├── User profiles with avatar
├── Online/offline status
└── User search

Messages
├── Private direct messages
├── Group chat conversations
├── Message history (paginated)
├── Edit/delete messages
├── Typing indicators
└── Read receipts

Notifications
├── New message alerts
├── Group mentions
├── User joined/left notifications
└── Sound notifications

Real-time Features (WebSockets)
├── Live message delivery
├── Presence updates
├── Typing indicators
└── Real-time user list
```

#### Generated API Endpoints
```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/users/search
POST   /api/conversations
GET    /api/conversations
GET    /api/conversations/{id}/messages
POST   /api/conversations/{id}/messages
POST   /api/conversations/{id}/messages/{msg_id}
DELETE /api/conversations/{id}/messages/{msg_id}
WS     /ws/{user_id}                (WebSocket)
```

---

### Example 5: Project Management Dashboard

#### Input Prompt
```
Build a project management tool with teams, projects, tasks, 
progress tracking, file attachments, and real-time collaboration 
using FastAPI and React.
```

#### Generated Database Schema
```
organizations
├── id, name, owner_id, description

teams
├── id, org_id, name, description

projects
├── id, team_id, name, description, status, start_date, end_date

tasks
├── id, project_id, title, description, status, priority, 
  assigned_to, due_date, created_at

subtasks
├── id, task_id, title, completed, created_at

attachments
├── id, task_id, file_url, uploaded_by, created_at

team_members
├── id, team_id, user_id, role, joined_at

comments
├── id, task_id, user_id, content, created_at
```

#### Generated Features
```
Organization Management
├── Create organization
├── Manage teams
├── Invite members
└── Set permissions

Project Planning
├── Create projects
├── Set timelines
├── Assign teams
└── Track progress

Task Management
├── Create tasks
├── Subtasks
├── Assign team members
├── Set priorities
├── Track status
└── Add due dates

Collaboration
├── Comments on tasks
├── File attachments
├── @mentions
├── Real-time updates
└── Activity timeline

Reporting
├── Project progress
├── Team workload
├── Burndown charts
└── Time tracking
```

---

## Code Quality Standards

All generated code includes:

### Backend Quality
- ✅ Type hints (Python 3.11+)
- ✅ Docstrings for all functions
- ✅ Error handling with try/except
- ✅ Logging statements
- ✅ Input validation with Pydantic
- ✅ Database transaction management
- ✅ RESTful API design
- ✅ CORS configuration

### Frontend Quality
- ✅ TypeScript with strict mode
- ✅ Component documentation
- ✅ Error boundaries
- ✅ Loading states
- ✅ Empty state handling
- ✅ Responsive design
- ✅ Accessibility (ARIA labels)
- ✅ CSS organization (Tailwind)

### DevOps Quality
- ✅ Multi-stage Docker builds
- ✅ Health checks
- ✅ Environment configuration
- ✅ Volume management
- ✅ Network isolation
- ✅ Resource limits
- ✅ Proper logging
- ✅ Production-ready

---

## Testing Approach

Generated projects include support for:

### Backend Testing
```python
# Backend tests template
import pytest
from fastapi.testclient import TestClient

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_item():
    response = client.post("/api/items", json={"title": "Test"})
    assert response.status_code == 201
```

### Frontend Testing
```typescript
// Frontend tests template
import { render, screen } from '@testing-library/react'

describe('Component', () => {
  it('renders correctly', () => {
    render(<Component />)
    expect(screen.getByText('Expected')).toBeInTheDocument()
  })
})
```

---

## Performance Characteristics

Generated applications typically achieve:

### Response Times
- API endpoints: 50-200ms (excluding LLM calls)
- Frontend page load: 1-2 seconds
- Database queries: 10-50ms

### Scalability
- Backend: Async/await support ready
- Database: Connection pooling configured
- Frontend: Code splitting enabled
- DevOps: Easy to scale with Kubernetes

### Security
- HTTPS-ready (configure in nginx/reverse proxy)
- CORS properly configured
- Input validation enforced
- SQL injection prevention
- XSS protection (React)
- CSRF token support

---

## Customization Examples

### Modifying Generated Code

#### Change Model Fields
```python
# Edit: generated_projects/{id}/backend/app/models.py
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    # Add custom field:
    priority = Column(String(50), default="medium")
    assigned_to = Column(String(255), nullable=True)
```

#### Add API Endpoint
```python
# Edit: generated_projects/{id}/backend/app/routes.py
@router.get("/api/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    # Your implementation
    return {"statistic": value}
```

#### Add Frontend Component
```typescript
// Create: generated_projects/{id}/frontend/components/Custom.tsx
export default function CustomComponent() {
  return <div>Custom content</div>
}
```

---

## Common Next Steps

After generation:

1. **Install Dependencies**
   ```bash
   cd generated_projects/{id}
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

2. **Run Locally**
   ```bash
   docker-compose up --build
   ```

3. **Customize**
   - Modify models and schemas
   - Add business logic
   - Extend UI components
   - Add tests

4. **Deploy**
   - Push to version control
   - Setup CI/CD
   - Deploy to cloud provider

---

## Output Consistency

AutoDev-AI ensures:

✅ All generated code follows same patterns
✅ Consistent naming conventions
✅ Standard project structure
✅ Proper documentation
✅ Working Docker setup
✅ Complete README
✅ Production-ready quality

---

**Example Generation Complete** ✅

All generated projects are:
- Fully functional
- Production-ready
- Customizable
- Documentable
- Deployable

---

*For actual generation, use the AutoDev-AI interface at http://localhost:3000*
