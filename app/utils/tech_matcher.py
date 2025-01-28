from geopy.distance import great_circle

def find_best_tech(service_request):
    eligible_techs = Technician.query.filter(
        Technician.is_available == True,
        Technician.certifications.any(
            Certification.test_type.ilike(f"%{service_request.service_type}%")
        )
    ).all()

    # Get request location from user profile
    user = User.query.get(service_request.user_id)
    
    ranked_techs = []
    for tech in eligible_techs:
        tech_coords = tuple(map(float, tech.location.split(',')))
        user_coords = tuple(map(float, user.address.coordinates.split(',')))  # Assuming address has coordinates
        
        distance = great_circle(user_coords, tech_coords).miles
        score = (tech.rating * 20) - (distance * 0.5)
        
        ranked_techs.append((tech, score))
    
    return sorted(ranked_techs, key=lambda x: x[1], reverse=True)[:3]